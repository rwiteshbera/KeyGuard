import sys
import os
import sqlite3

from src.compute.KeyDerivation import KeyDerivation

from rich import print as printC
from rich.console import Console


class VaultConnection:
    def __init__(self, vault_directory="./vault", vault_file="vault.db") -> None:
        self._vault_directory = vault_directory
        self._vault_file = vault_file
        self.vault_path = os.path.join(self._vault_directory, self._vault_file)
        
    # Check if the "vault" directory exists
    def checkVault(self):
        if not os.path.exists(self.vault_path):
            try:
                printC("[red]No vault found[/red]")
                sys.exit(0)

            except Exception as e:
                Console().print_exception()
                sys.exit(0)
    
    def createVault(self):
        if not os.path.exists(self.vault_path):
            try:
                os.mkdir(self.vault_path)

            except Exception as e:
                Console().print_exception()
                sys.exit(0)

    def connectVault(self):
        try:
            self.checkVault()
            return sqlite3.connect(self.vault_path)
        except Exception as e:
            Console().print_exception()
            sys.exit(0)


class VaultManager(VaultConnection):
    # Create 2 tables inside vault
    # secrets : To store admin login credentials
    # entry : Managing data inside the vault
    def createNewVault(self):
        print("Create a new vault:")
        try:
            # create Vault if not exists
            self.createVault()

            # Connect with vault
            vault = super().connectVault()
            cursor = vault.cursor()

            # Create Table
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS secrets (name TEXT NOT NULL, master_password_hash TEXT NOT NULL, phrase TEXT NOT NULL)")

            cursor.execute(
                "CREATE TABLE IF NOT EXISTS entries (name TEXT NOT NULL, token TEXT NOT NULL)")

            # Commit
            vault.commit()

            # Close the vault
            vault.close()

        except Exception as e:
            Console().print_exception()
            sys.exit(0)

    def configureVault(self, name: str, masterPassword: str):
        try:
            self.createNewVault()

            Key = KeyDerivation()

            # Generate Phrase
            phrase = os.urandom(16)

            # Compute Master Key from Unique phrase and MASTER PASSWORD
            masterKey = Key.computeMasterKey(
                payload=masterPassword.encode('utf-8'), salt=phrase)

            # Compute Master Password Hash from Master Key and MASTER PASSWORD
            # From (salt = MASTER PASSWORD, payload = Master Key) -> To (Master Password Hash)
            masterPasswordHash = Key.computeMasterPasswordHash(
                payload=masterKey, salt=masterPassword.encode('utf-8'),)

            # Connect with vault
            vault = super().connectVault()
            cursor = vault.cursor()

            # Insert data
            cursor.execute("INSERT INTO secrets (name, master_password_hash, phrase) VALUES (?, ?, ?)",
                           (name,  masterPasswordHash, phrase))

            # Commit
            vault.commit()

            printC("[green][+] Vault created successfully.")

            # Close the vault
            vault.close()

        except Exception as e:
            Console().print_exception()
            sys.exit(0)

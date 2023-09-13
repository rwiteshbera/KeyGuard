import sys
import os
import sqlite3

from src.compute.KeyDerivation import KeyDerivation

from rich import print as printC
from rich.console import Console
console = Console()


class VaultConnection:
    def __init__(self, vault_directory="./vault", vault_file="vault.db") -> None:
        self._vault_directory = vault_directory
        self._vault_file = vault_file

    # Check if the "vault" directory exists; if not, create it
    def __checkVaultDirectory(self):
        vault_path = os.path.join(self._vault_directory, self._vault_file)
        if not os.path.exists(self._vault_directory):
            try:
                os.mkdir(self._vault_directory)
            except Exception as e:
                console.print_exception()
                sys.exit(0)

        return vault_path

    def connectVault(self):
        try:
            vault_path = self.__checkVaultDirectory()
            return sqlite3.connect(vault_path)
        except Exception as e:
            printC("[red][!] An error occured while trying to configure vault")
            sys.exit(0)


class VaultManager(VaultConnection):
    # Create 2 tables inside vault
    # secrets : To store admin login credentials
    # entry : Managing data inside the vault
    def __CreateNewVault(self):
        print("Create a new vault:")
        try:
            # Connect with vault
            vault = super().connectVault()
            cursor = vault.cursor()

            # Create Table
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS secrets (email TEXT PRIMARY KEY, name TEXT NOT NULL, master_password_hash TEXT NOT NULL, vector TEXT NOT NULL)")

            cursor.execute(
                "CREATE TABLE IF NOT EXISTS entries (name TEXT PRIMARY KEY, token TEXT NOT NULL, admin TEXT NOT NULL, FOREIGN KEY (admin) REFERENCES secrets(email))")

            # Commit
            vault.commit()

            # Close the vault
            vault.close()

        except Exception as e:
            printC("[red][!] An error occured while trying to create vault")
            console.print_exception()
            sys.exit(0)

    def ConfigureVault(self, name: str, email: str, masterPassword: str):
        self.__CreateNewVault()
        try:
            Key = KeyDerivation()

            # Compute Master Key from Email and MASTER PASSWORD
            # From (salt = email, payload = MASTER PASSWORD) -> To (Master Key)
            masterKey = Key.computeMasterKey(
                salt=email.encode('utf-8'), payload=masterPassword.encode('utf-8'))

            # Compute Master Password Hash from Master Key and MASTER PASSWORD
            # From (salt = MASTER PASSWORD, payload = Master Key) -> To (Master Password Hash)
            masterPasswordHash = Key.computeMasterPasswordHash(
                salt=masterPassword.encode('utf-8'), payload=masterKey)

            # Generate Vector
            vector = os.urandom(16)

            # Connect with vault
            vault = super().connectVault()
            cursor = vault.cursor()

            # Insert data
            cursor.execute("INSERT INTO secrets (name, email, master_password_hash, vector) VALUES (?, ?, ?, ?)",
                           (name, email, masterPasswordHash, vector))

            # Commit
            vault.commit()

            printC("[green][+] Vault created successfully.")

            # Close the vault
            vault.close()

        except Exception as e:
            printC("[red][!] An error occured while trying to configure vault")
            console.print_exception()
            sys.exit(0)

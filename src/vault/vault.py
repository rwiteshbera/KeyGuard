import sys
import os
import sqlite3

from src.compute.DeviceId import getDeviceId
from src.compute.KeyDerivation import KeyDerivation
from src.compute.DeviceId import getDeviceId
from src.compute.AESCipher import AESCipher

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
            return False
        return True

    def createVault(self):
        if not os.path.exists(self._vault_directory):
            try:
                os.mkdir(self._vault_directory)

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
                "CREATE TABLE IF NOT EXISTS secrets (name TEXT NOT NULL, master_password_hash TEXT NOT NULL, phrase TEXT NOT NULL, device TEXT NOT NULL)")

            cursor.execute(
                "CREATE TABLE IF NOT EXISTS entries (name TEXT PRIMARY KEY, token TEXT NOT NULL)")

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
            aes = AESCipher()

            # Generate Phrase
            phrase = os.urandom(16)

            # Get Device id
            deviceId = getDeviceId()

            # Compute Master Key from Unique phrase and MASTER PASSWORD
            masterKey = Key.computeMasterKey(
                payload=masterPassword.encode('utf-8'), salt=phrase)

            # Compute Master Password Hash from Master Key and MASTER PASSWORD
            masterPasswordHash = Key.computeMasterPasswordHash(
                payload=masterKey, salt=masterPassword.encode('utf-8'),)

            # Connect with vault
            vault = super().connectVault()
            cursor = vault.cursor()

            # Insert data
            cursor.execute("INSERT INTO secrets (name, master_password_hash, phrase, device) VALUES (?, ?, ?, ?)",
                           (name,  masterPasswordHash, phrase, deviceId))

            # Commit
            vault.commit()

            printC("[green][+] Vault created successfully.")

            # Close the vault
            vault.close()

        except Exception as e:
            Console().print_exception()
            sys.exit(0)


def VerifyDevice(deviceId: str) -> bool:
    # Verify Device
    if (deviceId != getDeviceId()):
        return False
    return True

import sys
from getpass import getpass

from src.compute.pbkdf2 import computeMasterKey
from src.compute.pbkdf2 import computeMasterPasswordHash

from src.config.vault import connectVault
from src.input.input import setName
from src.input.input import setEmail
from src.input.input import setMasterPassword

from rich import print as printC
from rich.console import Console
console = Console()

# Create 2 tables inside vault
# secrets : To store admin login credentials
# entry : Managing data inside the vault


def __CreateNewVault():
    print("Create a new vault:")
    try:
        # Connect with vault
        vault = connectVault()
        cursor = vault.cursor()

        # Create Table
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS secrets (email TEXT PRIMARY KEY, name TEXT NOT NULL, master_password_hash TEXT NOT NULL)")

        cursor.execute(
            "CREATE TABLE IF NOT EXISTS entries (name TEXT NOT NULL, token TEXT NOT NULL)")

        # Commit
        vault.commit()

        # Close the vault
        vault.close()

    except Exception as e:
        printC("[red][!] An error occured while trying to create vault")
        sys.exit(0)


def ConfigureVault():
    __CreateNewVault()
    try:
        name = setName()
        email = setEmail()
        masterPassword = setMasterPassword()

        # Compute Master Key from Email and MASTER PASSWORD
        # From (salt = email, payload = MASTER PASSWORD) -> To (Master Key)
        masterKey = computeMasterKey(
            salt=email.encode('utf-8'), payload=masterPassword.encode('utf-8'))

        # Compute Master Password Hash from Master Key and MASTER PASSWORD
        # From (salt = MASTER PASSWORD, payload = Master Key) -> To (Master Password Hash)
        masterPasswordHash = computeMasterPasswordHash(
            salt=masterPassword.encode('utf-8'), payload=masterKey)

        # Connect with vault
        vault = connectVault()
        cursor = vault.cursor()

        # Insert data
        cursor.execute("INSERT INTO secrets (name, email, master_password_hash) VALUES (?, ?, ?)",
                       (name, email, masterPasswordHash))

        # Commit
        vault.commit()

        # Close the vault
        vault.close()

    except Exception as e:
        printC("[red][!] An error occured while trying to configure vault")
        sys.exit(0)

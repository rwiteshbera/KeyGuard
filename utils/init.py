import sys
from getpass import getpass

from compute.pbkdf2 import computeMasterKey
from compute.pbkdf2 import computeMasterPasswordHash

from rich import print as printC
from rich.console import Console
console = Console()

def CreateNewVault():
    try:
        printC("[green]PassGuard 2023 v0.1")
        print("Create a new vault:")

        # Enter User Email
        email = input("Email: ")

        # Enter MASTER PASSWORD
        masterPassword = getpass("Choose a MASTER PASSWORD: ")
        if masterPassword != getpass("Re-type: ") and masterPassword != "":
            printC("[yellow][-] Passworod doesn't match. [/yellow]")
            sys.exit(0)

        # Compute Master Key from Email and MASTER PASSWORD
        masterKey = computeMasterKey(
            salt=email.encode('utf-8'), payload=masterPassword.encode('utf-8'))

        # Compute Master Password Hash from Master Key and MASTER PASSWORD
        masterPasswordHash = computeMasterPasswordHash(
            salt=masterPassword.encode('utf-8'), payload=masterKey)

    except Exception as e:
        printC("[red][!] An error occured while trying to create database!")
        console.print_exception()
        sys.exit(0)

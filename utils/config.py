import sys
from getpass import getpass
import hashlib
import random
import string

from db.connect import connectDB
from db.connect import configDB

from utils.compute import computeMasterKey
from utils.compute import computeMasterPasswordHash

from rich import print as printC
from rich.console import Console
console = Console()


def Config():
    try:
        # Configure database
        configDB()

        # Connect database
        db = connectDB()
        if db is not None:
            cursor = db.cursor()

            printC("[green]PassGuard 2023 v0.1")
            print("Create an account")

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

            # Add them to Database
            query = "INSERT INTO passguard.secrets (email, masterPassword_hash) VALUES (%s, %s)"
            value = (email, masterPasswordHash)
            cursor.execute(query, value)
            db.commit()

            printC("[green][+] Configuration Done! [/green]")

            db.close()

    except Exception as e:
        printC("[red][!] An error occured while trying to create database!")
        console.print_exception()
        sys.exit(0)

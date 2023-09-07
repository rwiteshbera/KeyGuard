import sys
from getpass import getpass
import hashlib
import random
import string

from utils.db import connectDB

from rich import print as printC
from rich.console import Console
console = Console()


def generateDeviceSecret(length=10):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def Config():
    try:
        # Connect database
        db = connectDB()
        if db is not None:
            cursor = db.cursor()

            # Create Database
            cursor.execute("CREATE DATABASE IF NOT EXISTS passguard")
            printC("[green][+][/green] PassGuard Database has been created.")

            # Create Table
            query = "CREATE TABLE IF NOT EXISTS  passguard.secrets (masterPass_hash TEXT NOT NULL, device_secret TEXT NOT NULL)"
            res = cursor.execute(query)
            printC("[green][+][/green] Table 'secrets' has been created")

            query = "CREATE TABLE IF NOT EXISTS passguard.entries (name TEXT NOT NULL, token TEXT NOT NULL)"
            res = cursor.execute(query)
            printC("[green][+][/green] Table 'entries' has been created")

            masterPassword = ""
            while 1:
                masterPassword = getpass("Choose a MASTER PASSWORD: ")
                if masterPassword != getpass("Re-type: ") and masterPassword != "":
                    printC("[yellow][-] Passworod doesn't match. [/yellow]")
                    sys.exit(0)
                else:
                    break

            # Hash the MASTER PASSWORD
            hashed_masterPassword = hashlib.sha256(
                masterPassword.encode()).hexdigest()
            printC("[green][+] Generated hash of MASTER PASSWORD [/green] ")

            # Generate Device Secret
            secret = generateDeviceSecret()
            printC("[green][+] Device Secret Generated [/green]")

            # Add them to Database
            query = "INSERT INTO passguard.secrets (masterPass_hash, device_secret) VALUES (%s, %s)"
            value = (hashed_masterPassword, secret)
            cursor.execute(query, value)
            db.commit()

            printC("[green][+] Configuration Done! [/green]")

            db.close()
    except Exception as e:
        printC("[red][!] An error occured while trying to create database.")
        sys.exit(0)

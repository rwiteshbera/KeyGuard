import sys

from getpass import getpass


from db.connect import connectDB
from utils.aes import EncryptEntry

from rich import print as printC
from rich.console import Console
console = Console()


def AddNewEntry(name, siteurl, username, password):
    entry = {
        'name': name,
        'siteurl': siteurl,
        'username': username,
        'password': password,
    }

    token = EncryptEntry(str(entry).encode('utf-8'))

    try:
        # Connect Database
        db = connectDB()
        if db is not None:
            cursor = db.cursor()

            # Add them to Database
            query = "INSERT INTO passguard.entries (name, token) VALUES (%s, %s)"
            value = (name, token)
            cursor.execute(query, value)
            db.commit()

            printC("[green][+] Entry added! [/green]")

            db.close()
    except Exception as e:
        printC("[red][!] An error occured while trying to create database.")
        console.print_exception()
        sys.exit(0)




def RetrieveEntry(name):
    try:
        # Connect Database
        db = connectDB()
        if db is not None:
            cursor = db.cursor()

            # Add them to Database
            query = "SELECT token FROM passguard.entries WHERE name = %s"
            value = (name,)
            cursor.execute(query, value)

            for row in cursor:
                print(str(row[0]))
            
            db.close()
    except Exception as e:
        printC("[red][!] An error occured while trying to retrieve entry.")
        console.print_exception()
        sys.exit(0)
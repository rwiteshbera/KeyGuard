import sys

from getpass import getpass


from utils.db import connectDB
from utils.compute import computeMasterKey
from cryptography.fernet import Fernet

from rich import print as printC
from rich.console import Console
console = Console()





def AddNewEntry(masterPassword, secret, name, siteurl, username, password):
    masterKey = computeMasterKey(masterPassword, bytes(secret, "utf-8"))
    
    entry = {
        'name': name,
        'siteurl': siteurl,
        'username': username,
        'password': password,
    }

    f = Fernet(masterKey)
    token = f.encrypt(str(entry).encode('utf-8'))

    try:
        # Connect Database
        db = connectDB()
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
        print(e)
        sys.exit(0)




def RetrieveEntry(masterPassword, secret, name):
    try:
        # Connect Database
        db = connectDB()
        cursor = db.cursor()

         # Add them to Database
        query = "SELECT token FROM passguard.entries WHERE name = %s"
        value = (name,)
        cursor.execute(query, value)

        masterKey = computeMasterKey(masterPassword, bytes(secret, "utf-8"))
        f = Fernet(masterKey)

        for row in cursor:
            print(f.decrypt(row[0]).decode())
            
        db.close()
    except Exception as e:
        printC("[red][!] An error occured while trying to retrieve entry.")
        print(e)
        sys.exit(0)
import sys

from getpass import getpass

from src.compute.aes import EncryptAES256
from src.compute.entropy import generateSecretBits
from src.input.input import setEmail
from src.input.input import askMasterPassword
from src.compute.pbkdf2 import computeMasterKey
from src.config.vault import connectVault

from rich import print as printC
from rich.console import Console
console = Console()


def AddNewEntry():
    print("Login ")

    # Enter Email
    email = setEmail()

    # Ask MASTER PASSWORD
    masterPassword = askMasterPassword()

    print("\nAdd New Entry")
    name = input("name: ")
    siteurl = input("URL: ")
    username = input("Username: ")
    password = getpass("Password: ")

    entry = {"name": name, "siteurl": siteurl,
             "username": username, "password": password}

    # Compute Master Key from Email and MASTER PASSWORD
    # From (salt = email, payload = MASTER PASSWORD) -> To (Master Key)
    masterKey = computeMasterKey(
        salt=email.encode('utf-8'), payload=masterPassword.encode('utf-8'))
    initializationVector = generateSecretBits(128)

    token = EncryptAES256(data_bytes=str(entry).encode(
        'utf-8'), key=masterKey, iv=initializationVector)

    # Connect with vault
    vault = connectVault()
    cursor = vault.cursor()

    # Insert data
    cursor.execute("INSERT INTO entries (name, token, email, iv) VALUES (?, ?, ?, ?)",
                   (entry['name'], token, email, initializationVector))

    # Commit
    vault.commit()

    printC("[green][+] Entry created successfully.")

    # Close the vault
    vault.close()

    try:
        print()
    except Exception as e:
        printC("[red][!] An error occured while trying to create database.")
        console.print_exception()
        sys.exit(0)


def RetrieveEntry(name):
    try:
        print()
    except Exception as e:
        printC("[red][!] An error occured while trying to retrieve entry.")
        console.print_exception()
        sys.exit(0)

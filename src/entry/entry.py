import sys

from getpass import getpass

from src.compute.aes import EncryptAES256
from src.input.input import promptEmail
from src.input.input import promptMasterPassword
from src.compute.pbkdf2 import computeMasterKey
from src.compute.pbkdf2 import computeMasterPasswordHash
from src.compute.pbkdf2 import computeEncryptionKey
from src.config.vault import connectVault
from src.config.vault import readIV_from_file

from rich import print as printC
from rich.console import Console
console = Console()


def AddNewEntry():
    print("Login ")

    # Enter Email
    email = promptEmail()

    # Enter MASTER PASSWORD
    masterPassword = promptMasterPassword()

    print("\nAdd New Entry")
    name = input("name: ")
    siteurl = input("URL: ")
    username = input("Username: ")
    password = getpass("Password: ")

    data = {"name": name, "siteurl": siteurl,
             "username": username, "password": password}

    # Compute Master Key from Email and MASTER PASSWORD
    # From (salt = email, payload = MASTER PASSWORD) -> To (Master Key)
    masterKey = computeMasterKey(
        salt=email.encode('utf-8'), payload=masterPassword.encode('utf-8'))
    
    # Compute Master Password Hash from Master Key and MASTER PASSWORD
    # From (salt = MASTER PASSWORD, payload = Master Key) -> To (Master Password Hash)
    masterPasswordHash = computeMasterPasswordHash(
        salt=masterPassword.encode('utf-8'), payload=masterKey)
    
    encryptionKey = computeEncryptionKey(salt=masterKey, payload=masterPasswordHash)
    
    iv = readIV_from_file()

    # Encrypt using AES 256 - Symmetric
    token = EncryptAES256(data_bytes=str(data).encode(
        'utf-8'), key=encryptionKey, iv=iv)

    # Connect with vault
    vault = connectVault()
    cursor = vault.cursor()

    # Insert data
    cursor.execute("INSERT INTO entries (name, token, admin) VALUES (?, ?, ?)",
                   (data['name'], token, email))

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

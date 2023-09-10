import sys
import ast
import pyperclip

from getpass import getpass

from src.compute.aes import EncryptAES256
from src.compute.aes import DecryptAES256
from src.compute.pbkdf2 import computeMasterKey
from src.compute.pbkdf2 import computeMasterPasswordHash
from src.compute.pbkdf2 import computeEncryptionKey
from src.config.vault import connectVault

from rich import print as printC
from rich.console import Console
console = Console()


def AddNewEntry(email: str, masterPassword: str, name: str, siteurl: str, username: str, password: str):

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

    encryptionKey = computeEncryptionKey(
        salt=masterKey, payload=masterPasswordHash)

    # Connect with vault
    vault = connectVault()
    cursor = vault.cursor()

    res = cursor.execute(
        "SELECT vector FROM secrets WHERE email = ? ", (email,))
    iv = res.fetchone()

    # Encrypt using AES 256 - Symmetric
    token = EncryptAES256(data_bytes=str(data).encode(
        'utf-8'), key=encryptionKey, iv=iv[0])

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


def RetrieveEntry(email: str, masterPassword: str, name: str):
    try:
        # Connect with vault
        vault = connectVault()
        cursor = vault.cursor()

        token, vector = cursor.execute(
            'SELECT entries.token, secrets.vector FROM entries INNER JOIN secrets ON entries.admin = secrets.email WHERE entries.name = ? AND entries.admin = ?', (name, email,)).fetchone()

        masterKey = computeMasterKey(
            salt=email.encode('utf-8'), payload=masterPassword.encode('utf-8'))
        masterPasswordHash = computeMasterPasswordHash(
            salt=masterPassword.encode('utf-8'), payload=masterKey)
        encryptionKey = computeEncryptionKey(
            salt=masterKey, payload=masterPasswordHash)

        raw = DecryptAES256(token, key=encryptionKey, iv=vector)
        data = ast.literal_eval(raw.decode('utf-8'))

        password = data.get('password')

        if password is not None:
            del data['password']

            print(f"Name: {data['name']}")
            print(f"Siteurl: {data['siteurl']}")
            print(f"Username: {data['username']}")
            print()

            pyperclip.copy(password)
            printC("[green][+][/green] Password copied to clipboard")
        else:
            printC("[red][!] no password found")
            sys.exit(0)

    except Exception as e:
        printC("[red][!] An error occured while trying to retrieve entry.")
        console.print_exception()
        sys.exit(0)

import sys
import ast
import pyperclip
from getpass import getpass
from src.compute.KeyDerivation import KeyDerivation
from src.compute.AESCipher import AESCipher
from src.vault.vault import VaultManager

from rich import print as printC
from rich.console import Console


class EntryManager:
    def AddNewEntry(self, encryptionKey: bytes, phrase: bytes):
        try:
            print("\nAdd New Entry")
            name = input("name: ")
            siteurl = input("URL: ")
            username = input("Username: ")
            password = getpass("Password: ")

            data = {"name": name, "siteurl": siteurl,
                    "username": username, "password": password}

            # Connect with vault
            vault = VaultManager().connectVault()
            cursor = vault.cursor()

            aes = AESCipher()
            # Encrypt using AES 256 - Symmetric
            token = aes.EncryptAES256(data_bytes=str(data).encode(
                'utf-8'), key=encryptionKey, iv=phrase)
            
            encryptedName = aes.EncryptAES256(data_bytes=name.encode('utf-8'), key=encryptionKey, iv=phrase )

            # Insert data
            cursor.execute("INSERT INTO entries (name, token) VALUES (?, ?)",
                           (encryptedName, token))

            # Commit
            vault.commit()

            printC("[green][+] Entry created successfully.")

            # Close the vault
            vault.close()
        except Exception as e:
            Console().print_exception()
            sys.exit(0)

    def RetrieveEntry(self, encryptionKey: bytes, phrase: bytes):
        try:
            name = input("Name: ")
            
            aes = AESCipher()
            encryptedName = aes.EncryptAES256(data_bytes=name.encode('utf-8'), key=encryptionKey, iv=phrase )

            # Connect with vault
            vault = VaultManager().connectVault()
            cursor = vault.cursor()

            (token,) = cursor.execute(
                'SELECT token FROM entries WHERE name = ?', (encryptedName,)).fetchone()

            aes = AESCipher()
            raw = aes.DecryptAES256(token, key=encryptionKey, iv=phrase)
            data = ast.literal_eval(raw.decode('utf-8'))

            password = data.get('password')
            vault.close()

            if password is not None:
                del data['password']

                print(f"Siteurl: {data['siteurl']}")
                print(f"Username: {data['username']}")
                print()

                pyperclip.copy(password)
                printC("[green][+][/green] Password copied to clipboard")
            else:
                printC("[red][!] no password found")
                sys.exit(0)

        except Exception as e:
            Console().print_exception()
            sys.exit(0)

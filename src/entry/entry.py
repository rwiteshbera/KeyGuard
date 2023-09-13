import sys
import ast
import pyperclip

from src.compute.KeyDerivation import KeyDerivation
from src.compute.AESCipher import AESCipher
from src.vault.vault import VaultManager

from rich import print as printC
from rich.console import Console

class EntryManager:
    def AddNewEntry(self, email: str, masterPassword: str, name: str, siteurl: str, username: str, password: str):
        try:
            data = {"name": name, "siteurl": siteurl,
                    "username": username, "password": password}

            Key = KeyDerivation()

            # Compute Master Key from Email and MASTER PASSWORD
            # From (salt = email, payload = MASTER PASSWORD) -> To (Master Key)
            masterKey = Key.computeMasterKey(
                salt=email.encode('utf-8'), payload=masterPassword.encode('utf-8'))

            # Compute Master Password Hash from Master Key and MASTER PASSWORD
            # From (salt = MASTER PASSWORD, payload = Master Key) -> To (Master Password Hash)
            masterPasswordHash = Key.computeMasterPasswordHash(
                salt=masterPassword.encode('utf-8'), payload=masterKey)

            encryptionKey = Key.computeEncryptionKey(
                salt=masterKey, payload=masterPasswordHash)

            # Connect with vault
            vault = VaultManager().connectVault()
            cursor = vault.cursor()

            res = cursor.execute(
                "SELECT vector FROM secrets WHERE email = ? ", (email,))
            iv = res.fetchone()

            aes = AESCipher()
            # Encrypt using AES 256 - Symmetric
            token = aes.EncryptAES256(data_bytes=str(data).encode(
                'utf-8'), key=encryptionKey, iv=iv[0])

            # Insert data
            cursor.execute("INSERT INTO entries (name, token, admin) VALUES (?, ?, ?)",
                           (data['name'], token, email))

            # Commit
            vault.commit()

            printC("[green][+] Entry created successfully.")

            # Close the vault
            vault.close()
        except Exception as e:
            Console().print_exception()
            sys.exit(0)

    def RetrieveEntry(self, email: str, masterPassword: str, name: str):
        try:
            # Connect with vault
            vault = VaultManager().connectVault()
            cursor = vault.cursor()

            token, vector = cursor.execute(
                'SELECT entries.token, secrets.vector FROM entries INNER JOIN secrets ON entries.admin = secrets.email WHERE entries.name = ? AND entries.admin = ?', (name, email,)).fetchone()

            Key = KeyDerivation()
            masterKey = Key.computeMasterKey(
                salt=email.encode('utf-8'), payload=masterPassword.encode('utf-8'))
            masterPasswordHash = Key.computeMasterPasswordHash(
                salt=masterPassword.encode('utf-8'), payload=masterKey)
            encryptionKey = Key.computeEncryptionKey(
                salt=masterKey, payload=masterPasswordHash)

            aes = AESCipher()
            raw = aes.DecryptAES256(token, key=encryptionKey, iv=vector)
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

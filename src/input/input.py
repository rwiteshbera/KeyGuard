import sys
import string
import email_validator
from getpass import getpass
from src.vault.vault import VaultConnection
from src.compute.KeyDerivation import KeyDerivation
from rich import print as printC
from rich.console import Console


class Input:
    # Prompt for Name
    def setName(self):
        name = ""
        while (True):
            # Enter your name
            name = input("Name: ")
            if not name:
                printC("[yellow][!] Name cannot be empty. [/yellow]")
                continue
            else:
                # Remove leading and trailing spaces
                name = name.strip()
                break

        return name

    # Prompt for Email
    def setEmail(self):
        email = ""
        while (True):
            try:
                # Enter User Email
                email = input("Email: ")
                email = email.strip().lower()
                if not email:
                    printC("[yellow][!] Email cannot be empty. [/yellow]")
                    continue
                else:
                    email_info = email_validator.validate_email(email=email)
                    email = email_info.normalized
                    break

            except Exception as e:
                printC(
                    "[red][X] Invalid email. [/red]")
                self.setEmail()

        return email

    # Prompt for creating New Master Password
    def setNewMasterPassword(self, firstAttempt=True):
        if firstAttempt:
            print("\nMaster Password Rules:")
            print("- It must have 14 characters or more.")
            print("- It must contain at least one special character.")
            print("- It must contain at least one digit.")
            print("- It must contain at least one lowercase alphabet.")
            print("- It must contain at least one uppercase alphabet.")

        masterPassword = ""

        while (True):
            # Enter MASTER PASSWORD
            masterPassword = getpass("Choose a MASTER PASSWORD: ")
            if not masterPassword:
                printC("[yellow][!] Master Password cannot be empty. [/yellow]")
                continue
            else:
                # Remove leading and traling spaces
                masterPassword = masterPassword.strip()

                # It should not contain any space in the middle
                if ' ' in masterPassword:
                    printC("[yellow][!] Master Password cannot have space. [/yellow]")
                    continue

                break

        if self.isValidMasterPassword(masterPassword) == False:
            self.setNewMasterPassword(firstAttempt=False)

        while (True):
            if masterPassword != getpass("Re-type: "):
                printC("[yellow][-] Password doesn't match. [/yellow]")
            else:
                break

        return masterPassword

    # Prompt Master Password

    def setMasterPassword(self):
        masterPassword = ""

        while (True):
            # Enter MASTER PASSWORD
            masterPassword = getpass("MASTER PASSWORD: ")
            if not masterPassword:
                printC("[yellow][!] Master Password cannot be empty. [/yellow]")
                continue
            else:
                masterPassword = masterPassword.strip()
                break

        return masterPassword

    # Check if the master password is valid or not:
    # Rules:

    def isValidMasterPassword(self, masterPassword: str) -> bool:
        # In this dictionary 'rules', each rule [key] is associated with a tuple containing two elements - condition, message
        rules = {
            'count': (len(masterPassword) >= 14, '14 characters or more'),
            'character': (any(char in string.punctuation for char in masterPassword), '1 special character'),
            'digit': (any(char.isdigit() for char in masterPassword), '1 digit'),
            'lowercase_alphabet': (any(char.islower() for char in masterPassword), '1 lowercase alphabet'),
            'uppercase_alphabet': (any(char.isupper() for char in masterPassword), '1 uppercase alphabet')
        }

        valid = True

        for rule_name, (condition, requirement) in rules.items():
            if condition:
                printC(
                    f"[green][🗸] Master Password must have atleast {requirement} or more. [/green]")
            else:
                printC(
                    f"[yellow][!] Master Password must have atleast {requirement} or more. [/yellow]")
                valid = False

        return valid


# Verify Master Password


    def verifyMasterPassword(self, masterPassword: str):
        try:
            masterPassword = masterPassword.strip()

            # Connect with vault
            vault = VaultConnection().connectVault()
            cursor = vault.cursor()

            res = cursor.execute(
                'SELECT * FROM secrets').fetchall()

            if (len(res) == 0):
                printC("[red][-] No vault found")
                sys.exit(0)

            (name, master_password_hash_fromDB, phrase) = res[0]
            vault.close()

            Key = KeyDerivation()
            masterKey = Key.computeMasterKey(
                payload=masterPassword.encode('utf-8'), salt=phrase)

            masterPasswordHash = Key.computeMasterPasswordHash(
                payload=masterKey, salt=masterPassword.encode('utf-8'))
            
            if master_password_hash_fromDB != masterPasswordHash:
                printC("[red][-] Wrong Credentials")
                sys.exit(0)

            return (name, masterKey, masterPasswordHash, phrase)

        except Exception as e:
            Console().print_exception()
            sys.exit(0)

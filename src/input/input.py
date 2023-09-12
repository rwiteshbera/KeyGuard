import sys
import string
import email_validator
from getpass import getpass

from rich import print as printC
from rich.console import Console
console = Console()

# Prompt for Name


def promptName():
    name = ""
    while (True):
        # Enter your name
        name = input("Name: ")
        if not name:
            printC("[yellow][!] Name cannot be empty. [/yellow]")
            continue
        else:
            break

    return name

# Prompt for Email


def promptEmail():
    email = ""
    while (True):
        try:
            # Enter User Email
            email = input("Email: ")
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
            promptEmail()

    return email

# Prompt for creating New Master Password


def createNewMasterPassword(firstAttempt=True):
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
            break

    if isValidMasterPassword(masterPassword) == False:
        createNewMasterPassword(firstAttempt=False)

    while (True):
        if masterPassword != getpass("Re-type: "):
            printC("[yellow][-] Password doesn't match. [/yellow]")
        else:
            break

    return masterPassword


# Prompt Master Password
def promptMasterPassword():
    masterPassword = ""

    while (True):
        # Enter MASTER PASSWORD
        masterPassword = getpass("MASTER PASSWORD: ")
        if not masterPassword:
            printC("[yellow][!] Master Password cannot be empty. [/yellow]")
            continue
        else:
            break

    return masterPassword


# Check if the master password is valid or not:
# Rules:
def isValidMasterPassword(masterPassword: str) -> bool:
    warning = ['Master Password must have atleast',
               'or more.']

    rules = {'count': '14 characters',
             'character': '1 special character',
             'digit': '1 digit',
             'lowercase_alphabet': '1 lowercase alphabet',
             'uppercase_alphabet': '1 uppercase alphabet'
             }

    valid = True

    if len(masterPassword) < 14:
        printC(
            f"[yellow][!] {warning[0]} {rules['count']} {warning[1]} [/yellow]")
        valid = False
    else:
        printC(f"[green][🗸]{warning[0]} {rules['count']} {warning[1]}[/green]")

    if __validatePasswordRules(masterPassword, string.punctuation) == False:
        printC(
            f"[yellow][!] {warning[0]} {rules['character']} {warning[1]} [/yellow]")
        valid = False
    else:
        printC(
            f"[green][🗸]{warning[0]} {rules['character']} {warning[1]} [/green]")

    if __validatePasswordRules(masterPassword, string.digits) == False:
        printC(
            f"[yellow][!] {warning[0]} {rules['digit']} {warning[1]} [/yellow]")
        valid = False
    else:
        printC(
            f"[green][🗸]{warning[0]} {rules['digit']} {warning[1]} [/green]")

    if __validatePasswordRules(masterPassword, string.ascii_lowercase) == False:
        printC(
            f"[yellow][!] {warning[0]} {rules['lowercase_alphabet']} {warning[1]} [/yellow]")
        valid = False
    else:
        printC(
            f"[green][🗸]{warning[0]} {rules['lowercase_alphabet']} {warning[1]} [/green]")

    if __validatePasswordRules(masterPassword, string.ascii_uppercase) == False:
        printC(
            f"[yellow][!] {warning[0]} {rules['uppercase_alphabet']} {warning[1]} [/yellow]")
        valid = False
    else:
        printC(
            f"[green][🗸]{warning[0]} {rules['uppercase_alphabet']} {warning[1]} [/green]")

    return valid


def __validatePasswordRules(password: str, characters: str) -> bool:
    characterSet = set(characters)
    if len(characterSet.intersection(password)) == 0:
        return False
    return True

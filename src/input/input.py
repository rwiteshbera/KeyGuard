import sys
from getpass import getpass

from rich import print as printC
from rich.console import Console
console = Console()

# Prompt for Name
def promptName():
    name = ""
    for attempt in range(2):
        # Enter your name
        name = input("Name: ")
        if not name:
            if attempt == 0:
                printC("[yellow][!] Name cannot be empty. [/yellow]")
                continue
            elif attempt == 1:
                printC(
                    "[red][X] You didn't provide the required details. Exiting... [/red]")
                sys.exit(0)
        break

    if not name:
        printC(
            "[yellow][!] Exiting... [/yellow]")
        sys.exit(0)

    return name

# Prompt for Email
def promptEmail():
    email = ""
    for attempt in range(2):
        # Enter User Email
        email = input("Email: ")
        if not email:
            if attempt == 0:
                printC("[yellow][!] Email cannot be empty. [/yellow]")
                continue
            elif attempt == 1:
                printC(
                    "[red][X] You didn't provide the required details. Exiting... [/red]")
                sys.exit(0)
        break

    if not email:
        printC(
            "[yellow][!] Exiting... [/yellow]")
        sys.exit(0)

    return email

# Prompt for creating New Master Password
def createNewMasterPassword():
    masterPassword = ""
    for attempt in range(2):
        # Enter MASTER PASSWORD
        masterPassword = getpass("Choose a MASTER PASSWORD: ")
        if not masterPassword:
            if attempt == 0:
                printC("[yellow][!] Master Password cannot be empty. [/yellow]")
                continue
            elif attempt == 1:
                printC(
                    "[red][X] You didn't provide the required details. Exiting... [/red]")
                sys.exit(0)
        break

    if masterPassword != getpass("Re-type: "):
        printC("[yellow][-] Passworod doesn't match. [/yellow]")
        sys.exit(0)

    if not masterPassword:
        printC(
            "[yellow][!] Exiting... [/yellow]")
        sys.exit(0)

    return masterPassword


# Prompt Master Password
def promptMasterPassword():
    masterPassword = ""
    for attempt in range(2):
        # Enter MASTER PASSWORD
        masterPassword = getpass("MASTER PASSWORD: ")
        if not masterPassword:
            if attempt == 0:
                printC("[yellow][!] Master Password cannot be empty. [/yellow]")
                continue
            elif attempt == 1:
                printC(
                    "[red][X] You didn't provide the required details. Exiting... [/red]")
                sys.exit(0)
        break

    if not masterPassword:
        printC(
            "[yellow][!] Exiting... [/yellow]")
        sys.exit(0)

    return masterPassword

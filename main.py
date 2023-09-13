import sys

from getpass import getpass


from src.banner import DisplayBanner
from src.input.input import Input
from src.entry.entry import EntryManager
from src.vault.vault import VaultManager
from rich import print as printC
from rich.console import Console
console = Console()

if len(sys.argv) <= 1:
    sys.exit(0)

argument = sys.argv[1]

DisplayBanner()

if argument == "--add" or argument == '--a':
    prompt = Input()
    
    print("Login ")
    # Enter Email
    email = prompt.setEmail()

    # Enter MASTER PASSWORD
    masterPassword = prompt.setMasterPassword()

    # verifyMasterPassword
    prompt.verifyMasterPassword(email=email, masterPassword=masterPassword)

    print("\nAdd New Entry")
    name = input("name: ")
    siteurl = input("URL: ")
    username = input("Username: ")
    password = getpass("Password: ")

    EntryManager().AddNewEntry(email, masterPassword, name, siteurl, username, password)


elif argument == "--get" or argument == '--g':
    prompt = Input()
    # Enter Email
    email = input("email: ")

    # Ask MASTER PASSWORD
    masterPassword = prompt.setMasterPassword()

    # verifyMasterPassword
    prompt.verifyMasterPassword(email=email, masterPassword=masterPassword)

    name = input("Name: ")

    EntryManager().RetrieveEntry(email, masterPassword, name)

elif argument == "--init" or argument == "--i":
    prompt = Input()
    name = prompt.setName()
    email = prompt.setEmail()

    masterPassword = prompt.setNewMasterPassword()

    VaultManager().ConfigureVault(name, email, masterPassword)


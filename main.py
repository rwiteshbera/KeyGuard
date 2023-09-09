import sys

from getpass import getpass

from utils.entry import AddNewEntry
from utils.entry import RetrieveEntry
from utils.init import CreateNewVault

from rich import print as printC
from rich.console import Console
console = Console()

if len(sys.argv) <= 1:
    sys.exit(0)

argument = sys.argv[1]


if argument == "--add" or argument == '--a':
    # Enter Email
    email = input("email: ")

    # Ask MASTER PASSWORD
    masterPassword = getpass("Enter MASTER PASSWORD: ")

    print("Add new entry:")
    name = input("name: ")
    siteurl = input("URL: ")
    username = input("Username: ")
    password = getpass("Password: ")

    AddNewEntry(name, siteurl, username, password)


elif argument == "--get" or argument == '--g':
    # Enter Email
    email = input("email: ")

    # Ask MASTER PASSWORD
    masterPassword = getpass("Enter MASTER PASSWORD: ")

    name = input("Name: ")
    RetrieveEntry(name)

elif argument == "--init" or argument == "--i":
    CreateNewVault()
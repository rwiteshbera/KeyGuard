import sys

from getpass import getpass

from src.entry.entry import AddNewEntry
from src.entry.entry import RetrieveEntry
from src.config.init import ConfigureVault
from src.banner import DisplayBanner
from rich import print as printC
from rich.console import Console
console = Console()

if len(sys.argv) <= 1:
    sys.exit(0)

argument = sys.argv[1]

DisplayBanner()

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
    ConfigureVault()



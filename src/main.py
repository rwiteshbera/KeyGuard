import sys

from getpass import getpass

from utils.entry import AddNewEntry
from utils.entry import RetrieveEntry
from utils.config import Config


if len(sys.argv) <= 1:
    sys.exit(0)

argument = sys.argv[1]


if argument == "--add" or argument == '--a':
    # Ask MASTER PASSWORD
    masterPassword = getpass("Enter MASTER PASSWORD: ")

    print("Add new entry:")
    name = input("name: ")
    siteurl = input("URL: ")
    username = input("Username: ")
    password = getpass("Password: ")

    AddNewEntry(masterPassword, "abc", name, siteurl, username, password)


elif argument == "--get" or argument == '--g':
    # Ask MASTER PASSWORD
    masterPassword = getpass("Enter MASTER PASSWORD: ")

    name = input("Name: ")
    RetrieveEntry(masterPassword, "abc", name)

elif argument == "--config" or argument == "--c":
    Config()
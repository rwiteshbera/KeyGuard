import sys

from getpass import getpass

from src.compute.aes import EncryptEntry

from rich import print as printC
from rich.console import Console
console = Console()


def AddNewEntry(name, siteurl, username, password):
    entry = {
        'name': name,
        'siteurl': siteurl,
        'username': username,
        'password': password,
    }

    token = EncryptEntry(str(entry).encode('utf-8'))

    try:
        print()
    except Exception as e:
        printC("[red][!] An error occured while trying to create database.")
        console.print_exception()
        sys.exit(0)




def RetrieveEntry(name):
    try:
        print()
    except Exception as e:
        printC("[red][!] An error occured while trying to retrieve entry.")
        console.print_exception()
        sys.exit(0)
import sys

from getpass import getpass

from src.config.init import ConfigureVault
from src.entry.entry import AddNewEntry
from src.entry.entry import RetrieveEntry
from src.entry.entry import verifyMasterPassword

from src.banner import DisplayBanner
from src.input.input import promptName
from src.input.input import promptEmail
from src.input.input import createNewMasterPassword
from src.input.input import promptMasterPassword


from rich import print as printC
from rich.console import Console
console = Console()

if len(sys.argv) <= 1:
    sys.exit(0)

argument = sys.argv[1]

DisplayBanner()

if argument == "--add" or argument == '--a':
    print("Login ")
    # Enter Email
    email = promptEmail()

    # Enter MASTER PASSWORD
    masterPassword = promptMasterPassword()

    # verifyMasterPassword
    verifyMasterPassword(email=email, masterPassword=masterPassword)


    print("\nAdd New Entry")
    name = input("name: ")
    siteurl = input("URL: ")
    username = input("Username: ")
    password = getpass("Password: ")
    
    AddNewEntry(email, masterPassword, name, siteurl, username, password)


elif argument == "--get" or argument == '--g':
    # Enter Email
    email = input("email: ")

    # Ask MASTER PASSWORD
    masterPassword = promptMasterPassword()

    # verifyMasterPassword
    verifyMasterPassword(email=email, masterPassword=masterPassword)
    
    name = input("Name: ")

    RetrieveEntry(email, masterPassword, name)

elif argument == "--init" or argument == "--i":
    name = promptName()
    email = promptEmail()
    
    masterPassword = createNewMasterPassword()

    ConfigureVault(name, email, masterPassword)



import sys

from getpass import getpass


from src.banner import DisplayBanner
from src.login import Login
from src.login import Register
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
    (email, masterPassword) = Login()

    EntryManager().AddNewEntry(email, masterPassword)


elif argument == "--get" or argument == '--g':
    (email, masterPassword) = Login()

    EntryManager().RetrieveEntry(email, masterPassword)

elif argument == "--init" or argument == "--i":
    (name, email, masterPassword) = Register()

    VaultManager().ConfigureVault(name, email, masterPassword)

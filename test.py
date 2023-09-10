from src.config.init import ConfigureVault
from src.entry.entry import AddNewEntry
from src.entry.entry import RetrieveEntry
import shutil

from rich import print as printC
from rich.console import Console
console = Console()

name = "Rwitesh Bera"
email = "test@gmail.com"
masterPassword = "abc"

sitename = "Test"
siteurl = "https://www.test.com"
username = "test@gmail.com"
password = "test"

def test():
    try:
        ConfigureVault(name, email, masterPassword)
        AddNewEntry(email, masterPassword, sitename, siteurl, username, password)
        RetrieveEntry(email, masterPassword, sitename)
        shutil.rmtree("./vault")

        printC("\n[green][✔][/green] All tests passed")
    except:
        printC("\n[red][X] Checks failed")
        console.print_exception()

test()
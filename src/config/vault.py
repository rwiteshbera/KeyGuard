import sqlite3
import sys
import os

from src.compute.entropy import generateSecretBits
from rich import print as printC
from rich.console import Console
console = Console()


vault_directory = "./vault"
vault_file = "vault.db"

# Check if the "vault" directory exists; if not, create it


def __checkVaultDirectory():
    vault_path = os.path.join(vault_directory, vault_file)
    if not os.path.exists(vault_directory):
        try:
            os.mkdir(vault_directory)
        except Exception as e:
            console.print_exception()
            sys.exit(0)

    return vault_path

def connectVault():
    try:
        vault_path = __checkVaultDirectory()
        return sqlite3.connect(vault_path)
    except Exception as e:
        printC("[red][!] An error occured while trying to configure vault")
        sys.exit(0)

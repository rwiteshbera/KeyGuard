import sqlite3
import sys
import os

from src.compute.entropy import generateSecretBits
from rich import print as printC
from rich.console import Console
console = Console()


vault_directory = "./vault"
vault_file = "vault.db"
vault_iv = "iv.bin"

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


def writeIV_from_file():
    try:
        # Generate Initialization Vector and save
        iv = generateSecretBits(128)
        vault_iv_path = os.path.join(vault_directory, vault_iv)
        with open(vault_iv_path, 'wb') as file:
            file.write(iv)
        file.close()
    except:
        console.print_exception()
        sys.exit(0)


def readIV_from_file():
    try:
        iv = ""
        # Read IV from file
        vault_iv_path = os.path.join(vault_directory, vault_iv)
        with open(vault_iv_path, 'rb') as file:
            iv = file.read()
        file.close()
        return iv
    except:
        console.print_exception()
        sys.exit(0)


def connectVault():
    try:
        vault_path = __checkVaultDirectory()
        writeIV_from_file()

        return sqlite3.connect(vault_path)
    except Exception as e:
        printC("[red][!] An error occured while trying to configure vault")
        sys.exit(0)

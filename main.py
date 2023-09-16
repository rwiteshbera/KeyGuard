import sys
import argparse
from src.banner import DisplayBanner
from src.login import Login
from src.login import Register
from src.entry.entry import EntryManager
from src.vault.vault import VaultManager

class Main:
    def __init__(self) -> None:
        DisplayBanner()

    def run(self):
        parser = argparse.ArgumentParser(prog="PassGuard", description="Password Manager")
        parser.add_argument("--init", "--i", action="store_true", help="Initialize the vault")
        parser.add_argument("--add", "--a", action="store_true", help="Add a new entry to the vault")
        parser.add_argument("--get", "--g", action="store_true", help="Retrieve an entry from the vault")

        args = parser.parse_args()

        if args.init:
            (name, masterPassword) = Register()
            VaultManager().configureVault(name, masterPassword)

        elif args.add:
            (name, encryptionKey, phrase) = Login()
            EntryManager().AddNewEntry(encryptionKey=encryptionKey, phrase=phrase)

        elif args.get:
            (name, encryptionKey, phrase) = Login()
            EntryManager().RetrieveEntry(encryptionKey=encryptionKey, phrase=phrase)


if __name__ == "__main__":
    app = Main()
    app.run()
    
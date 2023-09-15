import sys

from src.banner import DisplayBanner
from src.login import Login
from src.login import Register
from src.entry.entry import EntryManager
from src.vault.vault import VaultManager

class Main:
    def __init__(self) -> None:
        DisplayBanner()

    def run(self):
        if len(sys.argv) <= 1:
            sys.exit(0)

        argument = sys.argv[1]

        if argument == "--init" or argument == "--i":
            (name, masterPassword) = Register()

            VaultManager().configureVault(name, masterPassword)

        elif argument == "--add" or argument == '--a':
            (name, encryptionKey, phrase) = Login()
            EntryManager().AddNewEntry(encryptionKey=encryptionKey, phrase=phrase)

        elif argument == "--get" or argument == '--g':
            (name, encryptionKey, phrase) = Login()
            EntryManager().RetrieveEntry(encryptionKey=encryptionKey, phrase=phrase)

if __name__ == "__main__":
    app = Main()
    app.run()
    
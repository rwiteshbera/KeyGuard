import unittest
import shutil
import os

from src.vault.vault import VaultManager
from src.entry.entry import EntryManager
from rich import print as printC
from rich.console import Console

class TestVaultOperations(unittest.TestCase):
    def setUp(self):
        self.name = "Rwitesh Bera"
        self.email = "testgmail.com"
        self.masterPassword = "abc"
        self.sitename = "Test"
        self.siteurl = "https://www.test.com"
        self.username = "test@gmail.com"
        self.password = "test"

    def test_vault_operations(self):
        try:
            # Configure the vault
            VaultManager().ConfigureVault(self.name, self.email, self.masterPassword)
            
            # Add a new entry to the vault
            e = EntryManager()
            e.AddNewEntry(self.email, self.masterPassword, self.sitename, self.siteurl, self.username, self.password)

            # Retrieve the entry from the vault
            e.RetrieveEntry(self.email, self.masterPassword, self.sitename)

            printC("\n[green][✔][/green] All tests passed")
        except Exception as e:
            printC("\n[red][X] Checks failed")
            printC(f"Error: {str(e)}")
            self.fail("Test failed")
        finally:
            # Clean up: Remove the vault directory
            shutil.rmtree("./vault")

if __name__ == '__main__':
    unittest.main()

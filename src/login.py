from src.input.input import Input
from src.compute.KeyDerivation import KeyDerivation
from src.vault.vault import VaultManager
from rich import print as printC
import sys

def Login():
    if VaultManager().checkVault() == False:
        printC("[red]No vault found[/red]")
        sys.exit(0)
    
    prompt = Input()
    
    print("Login ")

    # Enter MASTER PASSWORD
    masterPassword = prompt.setMasterPassword()

    # Verify Master Password
    (name, masterKey, masterPasswordHash, phrase) = prompt.verifyMasterPassword(masterPassword=masterPassword)

    Key = KeyDerivation()

    encryptionKey = Key.computeEncryptionKey(
                salt=masterKey, payload=masterPasswordHash)

    return (name, encryptionKey, phrase)


def Register():
    if VaultManager().checkVault():
        printC("[yellow] Vault already exists in your system. [/yellow]")
        sys.exit(0)

    prompt = Input()
    name = prompt.setName()

    masterPassword = prompt.setNewMasterPassword()

    return (name, masterPassword)
from src.input.input import Input
from src.compute.KeyDerivation import KeyDerivation
from src.vault.vault import VaultManager

def Login():
    VaultManager().checkVault()
    
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
    prompt = Input()
    name = prompt.setName()

    masterPassword = prompt.setNewMasterPassword()

    return (name, masterPassword)
from src.input.input import Input


def Login():
    prompt = Input()
    
    print("Login ")
    # Enter Email
    email = prompt.setEmail()

    # Enter MASTER PASSWORD
    masterPassword = prompt.setMasterPassword()

    # Verify Master Password
    prompt.verifyMasterPassword(email=email, masterPassword=masterPassword)

    return email, masterPassword


def Register():
    prompt = Input()
    name = prompt.setName()
    email = prompt.setEmail()

    masterPassword = prompt.setNewMasterPassword()

    return (name, email, masterPassword)
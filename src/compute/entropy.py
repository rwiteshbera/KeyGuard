import secrets
import mnemonic

mnemonic = mnemonic.Mnemonic("english")

def generateSecretBits(bits = 128) -> bytes:
    # Default = 128 bits
    return secrets.token_bytes(bits//8)


def getBIP39_codewords() -> str:
    # Generate 128-bit Entropy
    # (16 bytes = 16 x 8 = 128 bits)
    entropy = generateSecretBits()

    # Generate Mnemonic Words
    bip39_seeds = mnemonic.to_mnemonic(entropy)

    return bip39_seeds


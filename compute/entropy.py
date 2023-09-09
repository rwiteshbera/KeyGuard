import secrets
import mnemonic

mnemonic = mnemonic.Mnemonic("english")

def getBIP39_codewords() -> str:
    # Generate 128-bit Entropy
    # (16 bytes = 16 x 8 = 128 bits)
    entropy = secrets.token_bytes(16)

    # Generate Mnemonic Words
    bip39_seeds = mnemonic.to_mnemonic(entropy)

    return bip39_seeds


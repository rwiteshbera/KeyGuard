import base64
import string
import secrets

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

def __computePBKDF2HMAC(salt:bytes, payload: bytes, iteration=1) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iteration,
    )
    key = kdf.derive(payload)
    return base64.urlsafe_b64encode(key)


def computeMasterKey(salt: bytes, payload: bytes) -> bytes:
    return __computePBKDF2HMAC(salt=salt, payload=payload, iteration=100100)


def computeMasterPasswordHash(salt: bytes, payload: bytes) -> bytes:
    return __computePBKDF2HMAC(salt=salt, payload=payload, iteration=1)


def generateSalt(length=10) -> str:
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(length))

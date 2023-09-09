import base64
import string
import secrets

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes


def __computePBKDF2HMAC(algorithm, salt: bytes, payload: bytes, bits: int, iteration=1) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=algorithm,
        length=bits//8,
        salt=salt,
        iterations=iteration,
    )
    key = kdf.derive(payload)
    return key


def computeSeed(salt: bytes, payload: bytes) -> bytes:
    return __computePBKDF2HMAC(algorithm=hashes.SHA3_512(), salt=salt, payload=payload, iteration=2048, bits=512)


def computeMasterKey(salt: bytes, payload: bytes) -> bytes:
    return __computePBKDF2HMAC(algorithm=hashes.SHA256(), salt=salt, payload=payload, iteration=100100, bits=256)


def computeMasterPasswordHash(salt: bytes, payload: bytes) -> bytes:
    return __computePBKDF2HMAC(algorithm=hashes.SHA256(), salt=salt, payload=payload, iteration=1, bits=256)


def generateSalt(length=10) -> str:
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(length))

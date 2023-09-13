import sys
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from rich.console import Console


class Compute:
    def computePBKDF2HMAC(self, algorithm, salt: bytes, payload: bytes, bits: int, iteration=1) -> bytes:
        try:
            kdf = PBKDF2HMAC(
                algorithm=algorithm,
                length=bits//8,
                salt=salt,
                iterations=iteration,
            )
            key = kdf.derive(payload)
            return key
        except Exception as e:
            Console().print_exception()
            sys.exit(0)


class KeyDerivation(Compute):
    def computeSeed(self, salt: bytes, payload: bytes) -> bytes:
        return super().computePBKDF2HMAC(algorithm=hashes.SHA3_512(), salt=salt, payload=payload, iteration=2048, bits=512)

    def computeMasterKey(self, salt: bytes, payload: bytes) -> bytes:
        return super().computePBKDF2HMAC(algorithm=hashes.SHA256(), salt=salt, payload=payload, iteration=100100, bits=256)

    def computeMasterPasswordHash(self, salt: bytes, payload: bytes) -> bytes:
        return super().computePBKDF2HMAC(algorithm=hashes.SHA256(), salt=salt, payload=payload, iteration=1, bits=256)

    def computeEncryptionKey(self, salt: bytes, payload: bytes) -> bytes:
        return super().computePBKDF2HMAC(algorithm=hashes.SHA256(), salt=salt, payload=payload, iteration=100, bits=256)

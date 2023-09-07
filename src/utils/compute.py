import base64

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes


def computeMasterKey(masterPassword, secret):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=secret,
        iterations=600000,
    )
    key = kdf.derive(masterPassword.encode('utf-8'))

    return base64.urlsafe_b64encode(key)
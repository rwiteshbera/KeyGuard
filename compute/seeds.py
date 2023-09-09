from entropy import getBIP39_codewords
from pbkdf2 import computeSeed


codeWords = getBIP39_codewords()

payload = codeWords.encode('utf-8')
salt = "mnemonic".encode('utf-8')

masterSeed = computeSeed(salt=salt, payload=payload).hex()

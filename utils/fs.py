def writeFile(data_bytes: bytes):
    binary = open("vault.txt", "wb")

    binary.write(data_bytes)

    binary.close()


def readFile(path):
    file = open(path, "rb")
    try:
        data_bytes = file.read(1)
        while data_bytes != "":
            print(data_bytes)
    finally:
        file.close

writeFile(b'hello')
readFile('vault.txt')
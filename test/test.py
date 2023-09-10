import bcrypt

salt = bcrypt.gensalt()
password = 'abc'.encode()
print(salt)
print(bcrypt.hashpw(password, salt))
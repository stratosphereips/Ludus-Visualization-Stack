from cryptography.fernet import Fernet

## key
key = Fernet.generate_key()
print(key)

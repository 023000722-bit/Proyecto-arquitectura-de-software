from cryptography.fernet import Fernet

# Generate a symmetric key and create a Fernet instance
key = Fernet.generate_key()
f = Fernet(key)

# Encrypt a sample message used in the unit tests
token = f.encrypt(b"A really secret message. Not for prying eyes.")

# Expose a small helper (optional) for manual runs
if __name__ == "__main__":
    print("Key:", key)
    print("Token:", token)
from cryptography.fernet import Fernet


def generate_key() -> bytes:
    return Fernet.generate_key()


def get_fernet(key: bytes) -> Fernet:
    return Fernet(key)

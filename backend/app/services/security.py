from cryptography.fernet import Fernet

from ..config import get_settings

_settings = get_settings()


def _get_fernet() -> Fernet:
    return Fernet(_settings.FERNET_KEY)


def encrypt_secret(secret: str) -> str:
    return _get_fernet().encrypt(secret.encode()).decode()


def decrypt_secret(token: str) -> str:
    return _get_fernet().decrypt(token.encode()).decode()

import os
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

key = base64.b64decode(os.environ.get("AESGEM_KEY"))
aesgcm = AESGCM(key)

def encrypt_value(value: str) -> bytes:
    if not value:
        return None
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, value.encode('utf-8'), None)
    return nonce + ciphertext

def decrypt_value(data: bytes) -> str:
    if not data:
        return None
    nonce = data[:12]
    ciphertext = data[12:]
    return aesgcm.decrypt(nonce, ciphertext, None).decode('utf-8')
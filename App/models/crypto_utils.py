import os
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Load and decode AES-GCM key from environment variable
# Make sure AESGCM_KEY is a base64-encoded 32-byte (256-bit) key
raw_key = os.environ.get("AESGCM_KEY")
if not raw_key:
    raise RuntimeError("AESGCM_KEY is not set in environment variables.")

try:
    key = base64.b64decode(raw_key)
    if len(key) != 32:
        raise ValueError("AESGCM_KEY must decode to exactly 32 bytes (256 bits).")
except Exception as e:
    raise RuntimeError(f"Invalid AESGCM_KEY: {e}")

aesgcm = AESGCM(key)

def encrypt_value(value: str) -> bytes:
    """
    Encrypts a UTF-8 string using AES-GCM with a random nonce.
    Returns nonce + ciphertext as a single bytes object.
    """
    if value is None:
        return None
    if not isinstance(value, str):
        raise TypeError("encrypt_value expects a string.")
    
    nonce = os.urandom(12)  # 96-bit nonce required for AESGCM
    ciphertext = aesgcm.encrypt(nonce, value.encode('utf-8'), None)
    return nonce + ciphertext

def decrypt_value(data: bytes) -> str:
    """
    Decrypts a bytes object that contains nonce + ciphertext.
    Returns the original UTF-8 string.
    """
    if data is None:
        return None
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("decrypt_value expects a bytes-like object.")

    if len(data) < 13:  # At minimum, must contain a nonce + 1 byte ciphertext
        raise ValueError("Encrypted data is too short to contain valid nonce and ciphertext.")

    nonce = data[:12]
    ciphertext = data[12:]
    return aesgcm.decrypt(nonce, ciphertext, None).decode('utf-8')
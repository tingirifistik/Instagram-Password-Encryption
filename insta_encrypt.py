from base64 import b64encode
from time import time
from hashlib import blake2b
from urllib.parse import quote
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from nacl import public, utils
from nacl.bindings import crypto_box


def format_public_key(aes_key, receiver_pub_key):
    sender_sk = public.PrivateKey.generate()
    sender_pk = sender_sk.public_key
    nonce = blake2b(sender_pk.encode() + receiver_pub_key, digest_size=24).digest()
    sealed = crypto_box(aes_key, nonce, receiver_pub_key, sender_sk.encode())
    return sender_pk.encode() + sealed

def encrypt_password(password, version = "10", key_id = "143", public_key_hex = "f219393f2381eab7abd6d20130bfa274cc4ffc8b67988da60abeffc88c1b9b15"):
    password_bytes = password.encode("utf-8")
    timestamp = str(int(time()))
    timestamp_bytes = timestamp.encode("utf-8")

    if len(public_key_hex) != 64:
        raise ValueError("Public key must be 64-character hex string")

    public_key_bytes = bytes.fromhex(public_key_hex)
    
    if len(public_key_bytes) != 32:
        raise ValueError("Decoded public key must be 32 bytes")

    key_id_byte = int(key_id)
    aes_key = utils.random(32)
    iv = b"\x00" * 12
    encryptor = Cipher(algorithms.AES(aes_key), modes.GCM(iv), backend=default_backend()).encryptor()
    encryptor.authenticate_additional_data(timestamp_bytes)
    ciphertext = encryptor.update(password_bytes) + encryptor.finalize()
    tag = encryptor.tag
    encrypted_key = format_public_key(aes_key, public_key_bytes)

    if len(encrypted_key) != 80:
        raise ValueError("Encrypted AES key must be 80 bytes")

    total_len = 1 + 1 + 2 + 80 + 16 + len(ciphertext)
    output = bytearray(total_len)

    offset = 0
    output[offset] = 1
    offset += 1
    output[offset] = key_id_byte
    offset += 1
    output[offset] = len(encrypted_key) & 0xFF
    output[offset + 1] = (len(encrypted_key) >> 8) & 0xFF
    offset += 2
    output[offset:offset + 80] = encrypted_key
    offset += 80
    output[offset:offset + 16] = tag
    offset += 16
    output[offset:] = ciphertext

    encoded = b64encode(output).decode("utf-8")
    encrypted = f"#PWD_INSTAGRAM_BROWSER:{version}:{timestamp}:{encoded}"
    encrypted_encoded = quote(encrypted, safe="")
    return encrypted_encoded


if __name__ == "__main__":
    print(encrypt_password("your_password"))
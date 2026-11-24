"""Demonstrate SHA-256 verification and AES-GCM with a text message."""

import base64
import hashlib
import hmac
import secrets

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


NONCE_LENGTH = 12
DIGEST_LENGTH = 32


def encrypt_message(message: bytes, key: bytes) -> tuple[str, str]:
    """Return a Base64 packet and the SHA-256 digest for display."""
    digest = hashlib.sha256(message).digest()
    nonce = secrets.token_bytes(NONCE_LENGTH)
    ciphertext = AESGCM(key).encrypt(nonce, digest + message, None)
    packet = base64.b64encode(nonce + ciphertext).decode("ascii")
    return packet, digest.hex()


def decrypt_and_verify(packet: str, key: bytes) -> tuple[bytes, str]:
    """Return the recovered message only after authentication and hash verification."""
    packet_bytes = base64.b64decode(packet, validate=True)
    nonce = packet_bytes[:NONCE_LENGTH]
    ciphertext = packet_bytes[NONCE_LENGTH:]
    plaintext = AESGCM(key).decrypt(nonce, ciphertext, None)

    original_digest = plaintext[:DIGEST_LENGTH]
    message = plaintext[DIGEST_LENGTH:]
    received_digest = hashlib.sha256(message).digest()
    if not hmac.compare_digest(original_digest, received_digest):
        raise ValueError("The SHA-256 hashes do not match.")
    return message, received_digest.hex()


def main() -> int:
    print("Secure Data Transmission Demo")
    try:
        message = input("Enter a message: ").encode("utf-8")
    except (EOFError, KeyboardInterrupt):
        print("\nDemo canceled.")
        return 1

    # The sender and receiver share a key in memory for this local demo.
    key = AESGCM.generate_key(bit_length=256)
    packet, original_digest = encrypt_message(message, key)
    print(f"\nOriginal SHA-256:\n{original_digest}")
    print(f"\nAES-256-GCM packet (Base64):\n{packet}")
    try:
        input("\nPress Enter to receive and decrypt the packet...")
        recovered, received_digest = decrypt_and_verify(packet, key)
    except (EOFError, KeyboardInterrupt):
        print("\nDemo canceled.")
        return 1
    except (InvalidTag, ValueError):
        print("\nVerification failed. The message could not be verified.")
        return 1

    print(f"\nDecrypted message: {recovered.decode('utf-8')}")
    print(f"Recovered SHA-256:\n{received_digest}")
    print("Integrity check: PASS (SHA-256 hashes match)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

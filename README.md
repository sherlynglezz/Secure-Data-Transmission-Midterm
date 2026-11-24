# Secure Data Transmission App

**Sherlyn Hernandez · SDEV 245 · Module 4 Midterm**

This Python script takes a text message, hashes it with SHA-256, and encrypts the message and its hash together using AES-256-GCM. It simulates a sender passing a packet to a receiver in one terminal session. The receiver decrypts the packet, hashes the recovered message, and verifies that the two hashes match.

## Run the app

Use Python 3.10 or later. In a VS Code terminal opened in this project folder, run these commands on Windows:

```powershell
py -m pip install -r requirements.txt
py secure_transmission.py
```

On macOS or Linux, use `python3` in place of `py`.

1. Type a message such as `This is my secure midterm message.` and press Enter.
2. The script prints the original SHA-256 hash and the encrypted packet as Base64. The packet contains a nonce, ciphertext, and an authentication tag.
3. Press Enter again to simulate receiving the packet. Confirm that the original message returns, the two SHA-256 values match, and the script prints `Integrity check: PASS`.

## Confidentiality, integrity, and availability

- **Confidentiality.** AES-256-GCM protects the message and its original hash inside the encrypted packet. Both sides need the same secret key. The script generates the key in memory and keeps it out of the packet and terminal output.
- **Integrity.** AES-GCM checks its authentication tag during decryption and rejects a modified packet or a packet opened with the wrong key. After successful decryption the script computes SHA-256 again and compares it with the original hash. The recovered message is displayed only once both checks succeed.
- **Availability.** The demo runs locally with Python and its dependency, so the sender and receiver demonstration can run offline. In a real deployment, an authorized receiver would need continued access to both the packet and the corresponding key. Losing the key would make the packet unreadable. This demo keeps the key in memory for a single run.

## Entropy and key generation

Entropy is the unpredictability in the random input used to generate cryptographic values. A key based on a predictable value, such as the current time, may be easier to guess even when using AES-256. The script uses `AESGCM.generate_key(bit_length=256)` for a fresh key each run and `secrets.token_bytes(12)` for a random 96-bit nonce. Both use cryptographically secure randomness. The nonce can travel with the encrypted packet and must never repeat with the same key. The demo encrypts one message per generated key.

## References

- [Python hashlib documentation](https://docs.python.org/3/library/hashlib.html)
- [Python secrets documentation](https://docs.python.org/3/library/secrets.html)
- [Cryptography AES-GCM documentation](https://cryptography.io/en/latest/hazmat/primitives/aead/#cryptography.hazmat.primitives.ciphers.aead.AESGCM)

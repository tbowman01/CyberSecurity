#!/usr/bin/env python3
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.backends import default_backend
from dataclasses import dataclass
from secrets import token_bytes

"""
This implementation is incorrect and is being
used for educational purposes only!

This implementation is insecure because
each plaintext encrypted is encrypted 
using the same key and initialization vector,
removing the avalanche impact supported in the CBC
cipher. Only the initial block of plaintext should by XORed
with the initializaton vector, while all following blocks should be
XORed with the ciphertext generated by the previous block.
The initialization vector for every new encryption application
shoud possess a completely different IV.
"""
@dataclass
class EncryptionManager(object):
    key:bytes = token_bytes(32)
    iv:bytes = token_bytes(16)

    def encrypt(self, plaintext: str) -> bytes:
        encryptor:Callable = Cipher(
            algorithms.AES(self.key),
            modes.CBC(self.iv),
            backend=default_backend()
        ).encryptor()
        padder = PKCS7(128).padder()
        padded_message = padder.update(plaintext)
        padded_message += padder.finalize()
        ciphertext:bytes = self.encryptor.update(padded_message)
        ciphertext += self.encryptor.finalize()
        return ciphertext

    def decrypt(self, ciphertext: bytes) -> bytes:
        decryptor:Callable  = Cipher(
            algorithms.AES(self.key),
            modes.CBC(self.iv),
            backend=default_backend()
        ).encryptor()
        unpadder = PKCS7(128).unpadder()
        padded_plaintext = decryptor.update(ciphertext)
        padded_plaintext += decryptor.finalize()
        plaintext:bytes = unpadder.update(padded_plaintext)
        plaintext += unpadder.finalize()
        return plaintext

if __name__ == "__main__":
    manager = EncryptionManager()
    
    sample_text = [
        b"SHORT",
        b"MEDIUM MEDIUM MEDIUM",
        b"LONG LONG LONG LONG LONG LONG"
    ]

    ciphertexts = []
    for text in sample_text:
        ciphertexts.append(manager.encrypt(text))

    for cipher in ciphertexts:
        print("Recovered:", manager.decrypt(cipher))

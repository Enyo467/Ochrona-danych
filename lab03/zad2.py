from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

def encrypt_with_password(data, password):
    salt = get_random_bytes(16)
    iv = get_random_bytes(16)
    key = PBKDF2(
        password=password.encode("utf-8"),
        salt=salt,
        dkLen=32,
        count=200_000,
        hmac_hash_module=SHA256
    )
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(data, AES.block_size))
    return ciphertext, salt, iv

def decrypt_with_password(ciphertext, password, salt, iv) -> bytes:
    key = PBKDF2(
        password=password.encode("utf-8"),
        salt=salt,
        dkLen=32,
        count=200_000,
        hmac_hash_module=SHA256
    )
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ciphertext), AES.block_size)


password = "MojeHasloTestowe2026!"

with open("wiadomosc.txt", "rb") as f:
    file_data = f.read()

test_cases = [
    ("Puste dane (0 B)", b""),
    ("16 B ASCII", b"0123456789ABCDEF"),
    ("Plik wiadomosc.txt", file_data)
]

for name, data in test_cases:
    c, salt, iv = encrypt_with_password(data, password)
    dec = decrypt_with_password(c, password, salt, iv)
    print(f"\nTest: {name}")
    print(f"Rozmiar wejścia: {len(data)} B -> Długość kryptogramu: {len(c)} B")
    print(f"Zgodność danych (odszyfrowane == wejście): {dec == data}")

c1, _, _ = encrypt_with_password(file_data, password)
c2, _, _ = encrypt_with_password(file_data, password)
print(f"\nCzy kryptogramy są identyczne?: {c1 == c2}")

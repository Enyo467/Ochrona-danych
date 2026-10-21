from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


text = b"0123456789ABCDEF" * 4
key = bytes.fromhex("000102030405060708090a0b0c0d0e0f")

cipher_ecb = AES.new(key, AES.MODE_ECB)
ciphertext_ecb = cipher_ecb.encrypt(text)

iv = get_random_bytes(16)
cipher_cbc = AES.new(key, AES.MODE_CBC, iv)
ciphertext_cbc = cipher_cbc.encrypt(text)

blocks_ecb = []
for i in range(0, len(ciphertext_ecb), 16):
    block = ciphertext_ecb[i:i+16]
    blocks_ecb.append(block)

blocks_cbc = []
for i in range(0, len(ciphertext_cbc), 16):
    block = ciphertext_cbc[i:i+16]
    blocks_cbc.append(block)

print("Bloki w ECB:")
for i, b in enumerate(blocks_ecb, 1):
    print(f"Blok {i}: {b.hex()}")

print("Bloki w CBC:")
for i, b in enumerate(blocks_cbc, 1):
    print(f"Blok {i}: {b.hex()}")

decipher_ecb = AES.new(key, AES.MODE_ECB)
deciphertext_ecb = decipher_ecb.decrypt(ciphertext_ecb)

decipher_cbc = AES.new(key, AES.MODE_CBC, iv)
deciphertext_cbc = decipher_cbc.decrypt(ciphertext_cbc)

isecb = deciphertext_ecb == text
iscbc = deciphertext_cbc == text

print("Czy ecb został tak samo odszyfrowany:")
print(isecb)
print("Czy cbc został tak samo odszyfrowany:")
print(iscbc)

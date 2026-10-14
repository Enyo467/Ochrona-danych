import sys

def encrypt(data, key):
    result = bytearray()
    m = len(key)
    for i, b in enumerate(data):
        key_b = key[i % m]
        code = (b + key_b) % 256
        result.append(code)
    return bytes(result)

def decrypt(data, key):
    result = bytearray()
    m = len(key)
    for i, b in enumerate(data):
        key_b = key[i % m]
        uncode = (b - key_b) % 256
        result.append(uncode)
    return bytes(result)

def to_blocks(data, size=5):
    bloki = []
    for i in range(0, len(data), size):
        kawalek = data[i:i + size]
        bloki.append(kawalek.hex())
    return " ".join(bloki)

with open(sys.argv[1], "rb") as f:
    text_data = f.read()

key_zamek = b"ZAMEK"
cipher_zamek = encrypt(text_data, key_zamek)

with open("vigenere.bin", "wb") as f:
    f.write(cipher_zamek)

decrypted = decrypt(cipher_zamek, key_zamek)
print("Weryfikacja vigenere.bin:", decrypted == text_data)

assert decrypt(encrypt(b"", key_zamek), key_zamek) == b""
assert decrypt(encrypt(bytes([0, 255]), key_zamek), key_zamek) == bytes([0, 255])
print("Testy (puste dane, 0, 255): OK")

brama = b"BRAMABRAMABRAMA"
c_szyfr = encrypt(brama, b"SZYFR")
c_kod = encrypt(brama, b"KOD")

print("Klucz SZYFR:", to_blocks(c_szyfr, 5))
print("Klucz KOD:  ", to_blocks(c_kod, 5))
import string
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import math

def calculate_entropy(data):
    if not data:
        return 0.0

    length = len(data)
    
    counts = {}
    for byte in data:
        counts[byte] = counts.get(byte, 0) + 1

    entropy = 0.0
    for count in counts.values():
        p = count / length
        entropy -= p * math.log2(p)

    return entropy


with open("slaby_ecb.bin", "rb") as f:
    ciphertext = f.read()
    

sample = ciphertext[:4096]
charset = string.ascii_lowercase + string.digits

candidates = []
for char in charset:
    key = char.encode("ascii") * 16
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_sample = cipher.decrypt(sample)
    h = calculate_entropy(decrypted_sample)
    candidates.append((char, h))

candidates.sort(key=lambda x: x[1])

print("\n5 najlepszych kandydatów według entropii:")
for rank, (char, h) in enumerate(candidates[:5], 1):
    print(f"{rank}. Znak: '{char}' Entropia: {h:.4f} bitów/bajt")

best_char = candidates[0][0]
best_key = best_char.encode("ascii") * 16
full_cipher = AES.new(best_key, AES.MODE_ECB)
decrypted_full = full_cipher.decrypt(ciphertext)

unpadded_data = unpad(decrypted_full, AES.block_size)
plaintext = unpadded_data.decode("utf-8", errors="replace")
lines = plaintext.splitlines()
first_line = lines[0]
print(f"\nOdzyskany znak klucza: '{best_char}'")
print(f"Pierwszy wiersz tekstu: '{first_line}'")

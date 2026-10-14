import sys

with open(sys.argv[1], "rb") as f:
    data = f.read()

important_bytes = set(range(32, 127)) | {9, 10, 13}

total_bytes = len(data)

candidates = []

for k in range(256):
    txt = bytearray()
    for b in data:
        new_byte = (b - k) % 256
        txt.append(new_byte)

    decrypt = bytes(txt)

    valid_bytes = 0
    for b in decrypt:
        if b in important_bytes:
            valid_bytes +=1

    score = valid_bytes / total_bytes
    candidate = (score, k, decrypt)
    candidates.append(candidate)

def sorting(candidate):
    return(-candidate[0], candidate[1])

candidates.sort(key=sorting)

for i in range(5):
    candidate = candidates[i]
    score = candidate[0]
    k = candidate[1]
    txt = candidate[2]

    test_byte = txt[:50]
    test_txt = test_byte.decode("latin-1")

    procent = score * 100
    print(f"#{i+1} | k = {k:3d} | Trafność: {procent:6.2f}% | Tekst: {repr(test_txt)}")

best_k = 233

decrypt_txt = bytes((b - best_k) % 256 for b in data)

with open ("cezar.txt", "wb") as f:
    f.write(decrypt_txt)

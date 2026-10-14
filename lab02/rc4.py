import sys
import math
import time

sciezka_pliku = sys.argv[1]

def rc4(data, key) -> bytes:
    S = list(range(256))

    j = 0
    keylength = len(key)
    for i in range(256):
        j = (j + S[i] + key[i % keylength]) % 256
        S[i], S[j] = S[j], S[i]

    i = 0
    j = 0
    wynik = bytearray()
    
    for b in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        
        wynik.append(b ^ K)
        
    return bytes(wynik)

def oblicz_entropie(dane) -> float:
    if not dane:
        return 0.0
    dlugosc = len(dane)
    liczniki = {}
    for b in dane:
        liczniki[b] = liczniki.get(b, 0) + 1
    
    entropia = 0.0
    for wystapienia in liczniki.values():
        p = wystapienia / dlugosc
        entropia -= p * math.log2(p)
    return entropia

test_wejscie = b"Wiadomosc testowa 123"
test_klucz = b"abc"
assert rc4(rc4(test_wejscie, test_klucz), test_klucz) == test_wejscie
print("Weryfikacja symetrii RC4 (dwukrotne nałożenie): OK")

with open(sciezka_pliku, "rb") as f:
    kryptogram = f.read()

probka = kryptogram[:512]
litery = [chr(c) for c in range(ord('a'), ord('z') + 1)]

kandydaci = []
start = time.perf_counter()

for c1 in litery:
    for c2 in litery:
        for c3 in litery:
            klucz_str = c1 + c2 + c3
            klucz_bytes = klucz_str.encode("ascii")
            
            probne_dane = rc4(probka, klucz_bytes)
            h = oblicz_entropie(probne_dane)
            
            kandydaci.append((h, klucz_str, klucz_bytes))

czas_trwania = time.perf_counter() - start
liczba_prob = len(kandydaci)

def kryterium(kandydat):
    return (kandydat[0], kandydat[1])

kandydaci.sort(key=kryterium)

print(f"\nPrzeszukano {liczba_prob} kluczy w czasie {czas_trwania:.3f} s.")
for i in range(5):
    h, k_str, _ = kandydaci[i]
    print(f"#{i+1} | Klucz: '{k_str}' | Entropia: {h:.5f}")

najlepszy = kandydaci[0]
wybrany_klucz_str = najlepszy[1]
wybrany_klucz_bytes = najlepszy[2]

odszyfrowany_plik = rc4(kryptogram, wybrany_klucz_bytes)

with open("rc4.txt", "wb") as f:
    f.write(odszyfrowany_plik)

ponowne = rc4(odszyfrowany_plik, wybrany_klucz_bytes)
assert ponowne == kryptogram
print(f"\nWybrano klucz: '{wybrany_klucz_str}'")
print("Zgodność ponownego szyfrowania z kryptogramem: OK")
print(f"Entropia całego kryptogramu: {oblicz_entropie(kryptogram):.5f}")
print(f"Entropia całego tekstu:       {oblicz_entropie(odszyfrowany_plik):.5f}")
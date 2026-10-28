import hashlib

def oblicz_sha256_pliku(sciezka):
    with open(sciezka, 'rb') as plik:
        return hashlib.sha256(plik.read()).hexdigest()
try:
    with open("SHA256SUMS.txt", "r", encoding="utf-8") as plik_sum:
        for wiersz in plik_sum:
            wiersz = wiersz.strip()
            if not wiersz:
                continue
            
            oczekiwany_skrot, sciezka_pliku = wiersz.split("  ")
        
            try:
                aktualny_skrot = oblicz_sha256_pliku(sciezka_pliku)
                if aktualny_skrot == oczekiwany_skrot:
                    print(f"{sciezka_pliku}: OK")
                else:
                    print(f"{sciezka_pliku}: BŁĄD")
            except FileNotFoundError:
                print(f"{sciezka_pliku}: BRAK")
        

except FileNotFoundError:
    print("Plik SHA256SUMS.txt nie istnieje.")


skrot1 = hashlib.sha256(b"Ala ma kota.").digest()
skrot2 = hashlib.sha256(b"Ola ma kota.").digest()

roznice = 0
for bajt1, bajt2 in zip(skrot1, skrot2):
    xor = bajt1 ^ bajt2
    roznice += bin(xor).count('1')

print(f"Liczba różniących się bitów: {roznice}/256")
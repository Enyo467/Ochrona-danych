import hashlib
import hmac
import random

baza_hasel = {}

with open("hasla.txt", "r", encoding="utf-8") as plik:
    for wiersz in plik:
        wiersz = wiersz.strip()
        if wiersz:
            login, iteracje, sol_hex, skrot_hex = wiersz.split(":")
            baza_hasel[login] = (int(iteracje), sol_hex, skrot_hex)

def weryfikuj(login, haslo):
    if login not in baza_hasel:
        return False
        
    iteracje, sol_hex, zapisany_skrot_hex = baza_hasel[login]
    sol_bajty = bytes.fromhex(sol_hex)
    haslo_bajty = haslo.encode("utf-8")
    
    wyliczony_skrot = hashlib.pbkdf2_hmac("sha256", haslo_bajty, sol_bajty, iteracje, dklen=32)
    return hmac.compare_digest(wyliczony_skrot.hex(), zapisany_skrot_hex)

def dodaj(login, haslo):
    sol_bajty = random.randbytes(16)
    
    sol_hex = sol_bajty.hex()
    iteracje = 600000
    haslo_bajty = haslo.encode("utf-8")
    
    wyliczony_skrot = hashlib.pbkdf2_hmac("sha256", haslo_bajty, sol_bajty, iteracje, dklen=32)
    skrot_hex = wyliczony_skrot.hex()
    
    baza_hasel[login] = (iteracje, sol_hex, skrot_hex)
    return sol_hex, skrot_hex

print("anna, Kasztan-2026 ->", weryfikuj("anna", "Kasztan-2026"))
print("anna, kasztan-2026 ->", weryfikuj("anna", "kasztan-2026"))
print("piotr, Żółw na łące ->", weryfikuj("piotr", "Żółw na łące"))
print("kasia, Kasztan-2026 ->", weryfikuj("kasia", "Kasztan-2026"))

sol1, skrot1 = dodaj("test1", "eloEloeloElo123")
sol2, skrot2 = dodaj("test2", "eloEloeloElo123")

print(f"Czy sole są takie same? {sol1 == sol2}")
print(f"Czy skróty są takie same? {skrot1 == skrot2}")
print("test1 weryfikacja ->", weryfikuj("test1", "eloEloeloElo123"))
print("test2 weryfikacja ->", weryfikuj("test2", "eloEloeloElo123"))
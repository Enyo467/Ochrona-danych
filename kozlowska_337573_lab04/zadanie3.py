import hashlib

def h24(dane_bajty):
    return hashlib.sha256(dane_bajty).hexdigest()[:6]

def generuj_wariant(zawartosc_bajty, v):
    wiersze = zawartosc_bajty.split(b'\n')
    if wiersze and wiersze[-1] == b'':
        wiersze = wiersze[:-1]
        
    nowe_dane = bytearray()
    for i in range(13):
        if (v >> i) & 1 == 1:
            nowe_dane.extend(wiersze[i] + b' \n')
        else:
            nowe_dane.extend(wiersze[i] + b'\n')
            
    return bytes(nowe_dane)

with open("oryginal.txt", "rb") as plik_o:
    oryginal = plik_o.read()
    
with open("zmieniony.txt", "rb") as plik_z:
    zmieniony = plik_z.read()

slownik_oryg = {}
for v in range(8192):
    skrot = h24(generuj_wariant(oryginal, v))
    if skrot not in slownik_oryg:
        slownik_oryg[skrot] = v

hash_ustalony = h24(generuj_wariant(oryginal, 0))

znaleziona_para = None
licznik_ustalonego = 0

for v_z in range(8192):
    skrot_zmieniony = h24(generuj_wariant(zmieniony, v_z))
    
    if znaleziona_para is None and skrot_zmieniony in slownik_oryg:
        v_o = slownik_oryg[skrot_zmieniony]
        znaleziona_para = (v_o, v_z, skrot_zmieniony)
        
    if skrot_zmieniony == hash_ustalony:
        licznik_ustalonego += 1

print("Znaleziona kolizja (v_oryginal, v_zmieniony, h24):", znaleziona_para)
print("Liczba wariantów zmienionego pliku zgodnych z oryginałem v=0:", licznik_ustalonego)
#!/usr/bin/python3
import os

print("Content-Type: text/plain; charset=utf-8")

print()

print(f"UID: {os.geteuid()}")
print(f"GID: {os.getegid()}")

def czytaj(sciezka):
    try:
        with open(sciezka, 'r') as plik:
            return plik.read().strip()
    except Exception as e:
        return f"Odmowa odczytu ({e})"

print(f"Ogolny: {czytaj('/lab-data/ogolny.txt')}")
print(f"Poufny: {czytaj('/lab-data/poufny.txt')}")
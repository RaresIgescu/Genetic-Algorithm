import random
import string


#Functie pentru generarea unui numar aleator rounjit la p zecimale
def gen_numar_aleator(x: float, y: float, precizie: int) -> float:
    return round(random.uniform(x, y), precizie)

#Verifica daca un numar
def is_power_of_two(n: int) -> tuple[bool, int]:
    if n <= 0 or n % 2 != 0:
        return False, 0
    ct = 0
    while n % 2 == 0:
        n //= 2
        ct += 1
    return (n == 1), ct

def calculate_number(p: int, nr: float) -> float:
    while p > 0:
        nr *= 10
        p -= 1
    return nr

def calculate_l(l: int, nr: float) -> tuple[int, float]:
    while not is_power_of_two(int(nr))[0]:
        l = 0
        nr += 1
    return l, nr

def codificare(nr: int, lungime: int) -> list[int]:
    codif = [0] * lungime
    k = 0
    while nr > 0 and k < lungime:
        codif[k] = nr % 2
        nr //= 2
        k += 1
    return codif

def generare_sir_binar(x: int, discretizare: float, l: int, numarAleator: float) -> str:
    numar_de_codificat = int((numarAleator - x) / discretizare)
    codif = [0] * (l + 2)
    codif = codificare(numar_de_codificat, l + 2)
    rezultat = "".join(str(codif[i]) for i in range(l - 1,  -11, -1))
    return rezultat

def calculare_valoare_functie(a: int, b: int, c: int, numar_aleator: float) -> float:
    return (a * (numar_aleator * numar_aleator) + b * numar_aleator) + c

def main():

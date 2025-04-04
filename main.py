import random
import bisect
from typing import Tuple, List

# Functie pentru generarea unui numar aleator rounjit la p zecimale
def gen_numar_aleator(x: float, y: float, precizie: int) -> float:
    return round(random.uniform(x, y), precizie)

# Verifica daca un numar este putere a lui 2
def is_power_of_two(n: int) -> Tuple[bool, int]:
    ct = 0
    if n <= 0 or n % 2 != 0:
        return False, ct
    while n % 2 == 0:
        n //= 2
        ct += 1
    return (n == 1), ct

# Calculeaza Nr om functie de precizie
def calculate_number(p: int, nr: float) -> float:
    while p > 0:
        nr *= 10
        p -= 1
    return nr

# Calculeaza L necesar in functie de discretizare
def calculate_l(l: int, nr: float) -> Tuple[int, float]:
    while True:
        is_power, new_l = is_power_of_two(int(nr))
        if is_power:
            return new_l, nr
        l = 0
        nr += 1

# Codifica un numar in binar
def codificare(nr: int, lungime: int) -> List[int]:
    codif = [0] * lungime
    k = 0
    while nr > 0 and k < lungime:
        codif[k] = nr % 2
        nr //= 2
        k += 1
    return codif

# Genereaza sir binar pentru fiecare numar aleator
def generare_sir_binar(x: int, discretizare: float, l: int, numarAleator: float) -> str:
    numar_de_codificat = int((numarAleator - x) / discretizare)
    codif = [0] * l
    codif = codificare(numar_de_codificat, l)
    rezultat = "".join(str(codif[i]) for i in range(l - 1,  -1, -1))
    return rezultat

# Calculeaza valorea functiei pentru fiecare numar aleator generat
def calculare_valoare_functie(a: int, b: int, c: int, numar_aleator: float) -> float:
    return (a * (numar_aleator * numar_aleator) + b * numar_aleator) + c

def gasire_interval(x: float, intervale: List[float]) ->  float:
    i = bisect.bisect_right(intervale, x)
    if i == 0 or i >= len(intervale):
        raise ValueError(f"Numărul {x} este în afara intervalelor definite")
    return i

def main():
    # Citirea valorilor de intrare
    dimensiunePopulatie = int(input("Introduceti dimensiunea populatiei: "))
    x, y = map(int, input("Introduceti capetele intervalului (x y): ").split())  # Intervalul
    a, b, c = map(int, input("Introduceti parametrii functiei (a b c): ").split())  # Parametrii functiei
    precizie = int(input("Introduceti precizia: "))
    probabilitate_recombinare = float(input("Introduceti probabilitatea de recombinare: "))
    probabilitate_mutatie = float(input("Introduceti probabilitatea de mutatie: "))
    numar_etape = int(input("Introduceti numarul de etape: "))

    # Initializarea variabilelor
    valori_x = [0.0] * dimensiunePopulatie
    valori_noi_x = [0.0] * dimensiunePopulatie

    valori_functie = [0.0] * dimensiunePopulatie
    valori_noi_functie = [0.0] * dimensiunePopulatie

    sirBinar = [""] * dimensiunePopulatie
    sir_nou_binar = [""] * dimensiunePopulatie

    suma_totala_val_functie = 0.0
    probabilitati_selectie_cromozom = [0.0] * dimensiunePopulatie
    numere_uniforme = [0.0] * dimensiunePopulatie

    # Calcularea discretizarii si a valorii L
    nr = y - x
    nr = calculate_number(precizie, nr)
    l = 0
    l, nr = calculate_l(l, nr)
    discretizare = (y - x) / float(nr)

    #Populatia initiala
    with open("rezultate.txt", 'w') as f:
        for i in range(dimensiunePopulatie):
            #Valorea corespunzatoare cromozomului in domeniu de definitie
            valori_x[i] = gen_numar_aleator(x, y, precizie)

            #Reprezentarea pe biti a cromozomului
            sirBinar[i] = generare_sir_binar(x, discretizare, l, valori_x[i])

            #Valorea cromozomului, valorea functiei in punctul din domeniu
            valori_functie[i] = calculare_valoare_functie(a, b, c, valori_x[i])

            #Suma tuturor valorilor functiei
            suma_totala_val_functie += valori_functie[i]
            f.write(f"{i + 1:2d}: {sirBinar[i]} x= {valori_x[i]: .6f} f= {valori_functie[i]:.15f}\n")

        f.write("\n")
        f.write("Probabilitati selectie:\n")

        #Probabilitatea de selectie pentru fiecare cromozom
        for i in range(dimensiunePopulatie):
            probabilitati_selectie_cromozom[i] = valori_functie[i] / suma_totala_val_functie
            f.write(f"cromozom  {i + 1:2d} probabilitate {probabilitati_selectie_cromozom[i]}\n")

        f.write("\n")
        f.write("Suma totala:")
        f.write(f"{suma_totala_val_functie}\n")

        f.write("\n")
        f.write('Intervale probabilitati de selectie:\n')
        q = [0.0] * (dimensiunePopulatie + 1)
        q[0] = 0.0
        f.write(f'0.0\n')

        #Probabilitatile cumulate care dau intervalele de selectie
        for i in range(1, dimensiunePopulatie + 1):
            temp = q[i - 1]
            q[i] = temp + probabilitati_selectie_cromozom[i - 1]
            f.write(f'{q[i]}\n')

        f.write("\n")
        f.write('Nunerele uniforme: \n')
        for i in range(dimensiunePopulatie):
            numere_uniforme[i] = random.random()
            f.write(f"u = {numere_uniforme[i]:8} \t selectat cromozomul {gasire_interval(numere_uniforme[i], q):2d}\n")
            index = gasire_interval(numere_uniforme[i], q) - 1
            valori_noi_x[i] = valori_x[int(index)]
            valori_noi_functie[i] = valori_functie[int(index)]
            sir_nou_binar[i] = sirBinar[int(index)]

        f.write("\n")
        f.write('Dupa selectie: \n')
        for i in range(dimensiunePopulatie):
            f.write(f"{i + 1:2d}: {sir_nou_binar[i]} x= {valori_noi_x[i]: .6f} f= {valori_noi_functie[i]:.15f}\n")



if __name__ == "__main__":
    main()


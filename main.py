# import random
# import bisect
# from typing import Tuple, List
#
# # Funcții ajutătoare pentru operații matematice și de codificare
#
# def gen_numar_aleator(x: float, y: float, precizie: int) -> float:
#     return round(random.uniform(x, y), precizie)
#
# def is_power_of_two(n: int) -> Tuple[bool, int]:
#     ct = 0
#     if n <= 0 or n % 2 != 0:
#         return False, ct
#     while n % 2 == 0:
#         n //= 2
#         ct += 1
#     return (n == 1), ct
#
# def calculate_number(p: int, nr: float) -> float:
#     while p > 0:
#         nr *= 10
#         p -= 1
#     return nr
#
# def calculate_l(l: int, nr: float) -> Tuple[int, float]:
#     while True:
#         is_power, new_l = is_power_of_two(int(nr))
#         if is_power:
#             return new_l, nr
#         l = 0
#         nr += 1
#
# def codificare(nr: int, lungime: int) -> List[int]:
#     codif = [0] * lungime
#     k = 0
#     while nr > 0 and k < lungime:
#         codif[k] = nr % 2
#         nr //= 2
#         k += 1
#     return codif
#
# def generare_sir_binar(x: int, discretizare: float, l: int, numarAleator: float) -> str:
#     numar_de_codificat = int((numarAleator - x) / discretizare)
#     codif = codificare(numar_de_codificat, l)
#     rezultat = "".join(str(codif[i]) for i in range(l - 1, -1, -1))
#     return rezultat
#
# def calculare_valoare_functie(a: int, b: int, c: int, numar_aleator: float) -> float:
#     return (a * (numar_aleator * numar_aleator) + b * numar_aleator) + c
#
# def gasire_interval(x: float, intervale: List[float]) -> float:
#     i = bisect.bisect_right(intervale, x) # Vom folosi cautarea binara direct cu import
#     if i == 0 or i >= len(intervale):
#         raise ValueError(f"Numărul {x} este în afara intervalelor definite")
#     return i
#
# def decodificare(x: float, discretizare: float, sir: str) -> float:
#     numar = int(sir, 2)  # Conversie directă din binar în întreg
#     max_posibil = (1 << len(sir)) - 1  # Echivalent cu 2^len(sir) - 1
#     return x + (numar / max_posibil) * (discretizare * max_posibil)
#
# def initializare_populatie(dimensiune: int, x: int, y: int, precizie: int, a: int, b: int, c: int,
#                            discretizare: float, l: int, f) -> Tuple[List[float], List[str], List[float], float]:
#     """
#     Inițializează populația: pentru fiecare cromozom se generează valoarea lui x,
#     reprezentarea binară și se calculează valoarea funcției, acumulând suma totală.
#     """
#     valori_x = []
#     sirBinar = []
#     valori_functie = []
#     suma_totala = 0.0
#     for i in range(dimensiune):
#         x_val = gen_numar_aleator(x, y, precizie)
#         valori_x.append(x_val)
#         bin_str = generare_sir_binar(x, discretizare, l, x_val)
#         sirBinar.append(bin_str)
#         f_val = calculare_valoare_functie(a, b, c, x_val)
#         valori_functie.append(f_val)
#         suma_totala += f_val
#         f.write(f"{i + 1:2d}: {bin_str} x= {x_val} f= {f_val}\n")
#     return valori_x, sirBinar, valori_functie, suma_totala
#
# def calcul_probabilitati(valori_functie: List[float], f) -> Tuple[List[float], List[float]]:
#     """
#     Calculează probabilitățile de selecție pe baza valorilor funcției și construiește
#     intervalele cumulative.
#     """
#     suma_totala = sum(valori_functie)
#     probabilitati = [val / suma_totala for val in valori_functie]
#     f.write("\nProbabilitati selectie:\n")
#     for i, p in enumerate(probabilitati):
#         f.write(f"cromozom  {i + 1:2d} probabilitate {p}\n")
#     q = [0.0]
#     for p in probabilitati:
#         q.append(q[-1] + p)
#     f.write("\nIntervale probabilitati de selectie:\n")
#     for val in q:
#         f.write(f"{val}\n")
#     return probabilitati, q
#
# def selectie_populatie(dimensiune: int, q: List[float], valori_x: List[float],
#                         valori_functie: List[float], sirBinar: List[str], f) -> Tuple[List[float], List[float], List[str]]:
#     """
#     Selectează cromozomii pe baza numerelor uniforme și a intervalelor de selecție.
#     """
#     valori_noi_x = [0.0] * dimensiune
#     valori_noi_functie = [0.0] * dimensiune
#     sir_nou_binar = ["" for _ in range(dimensiune)]
#     f.write("\nNumerele uniforme si selectia cromozomilor:\n")
#     for i in range(dimensiune):
#         u = random.random()
#         index = int(gasire_interval(u, q)) - 1
#         f.write(f"u = {u:8} \t selectat cromozomul {index + 1:2d}\n")
#         valori_noi_x[i] = valori_x[index]
#         valori_noi_functie[i] = valori_functie[index]
#         sir_nou_binar[i] = sirBinar[index]
#     f.write("\nDupa selectie:\n")
#     for i in range(dimensiune):
#         f.write(f"{i + 1:2d}: {sir_nou_binar[i]} x= {valori_noi_x[i]} f= {valori_noi_functie[i]}\n")
#     return valori_noi_x, valori_noi_functie, sir_nou_binar
#
# def recombinare_populatie(dimensiune: int, probabilitate_recombinare: float, sir_nou_binar: List[str],
#                           valori_noi_x: List[float], valori_noi_functie: List[float],
#                           x: int, discretizare: float, precizie: int, a: int, b: int, c: int, f) -> None:
#     """
#     Efectuează procesul de recombinare: selectează cromozomii care vor participa,
#     efectuează schimbul de gene la un punct aleator și actualizează valorile.
#     """
#     f.write(f"\nProbabilitate de recombinare: {probabilitate_recombinare}\n")
#     participanti = []
#     index_participanti = []
#     for i in range(dimensiune):
#         u = random.random()
#         if u < probabilitate_recombinare / 100:
#             f.write(f'{i + 1}: {sir_nou_binar[i]} u= {u} < {probabilitate_recombinare} participa\n')
#             participanti.append(sir_nou_binar[i])
#             index_participanti.append(i)
#         else:
#             f.write(f'{i + 1}: {sir_nou_binar[i]} u= {u}\n')
#     if len(participanti) % 2 != 0:
#         # Dacă numărul este impar, eliminăm ultimul participant
#         participanti.pop()
#         index_participanti.pop()
#     f.write("\nProcesul de recombinare:\n")
#     for i in range(0, len(index_participanti), 2):
#         idx1 = index_participanti[i]
#         idx2 = index_participanti[i+1]
#         f.write(f"Recombinare dintre cromozomul {idx1 + 1} cu cromozomul {idx2 + 1}:\n")
#         f.write(f"{sir_nou_binar[idx1]} {sir_nou_binar[idx2]} ")
#         punct = random.randint(0, len(sir_nou_binar[0]))
#         f.write(f"punct {punct}\nRezultat: \n")
#         if punct != 0:
#             lista1 = list(sir_nou_binar[idx1])
#             lista2 = list(sir_nou_binar[idx2])
#             for j in range(punct, len(lista1)):
#                 lista1[j], lista2[j] = lista2[j], lista1[j]
#             sir_nou_binar[idx1] = ''.join(lista1)
#             sir_nou_binar[idx2] = ''.join(lista2)
#             # Actualizează valorile x și funcția corespunzătoare
#             valori_noi_x[idx1] = round(decodificare(x, discretizare, sir_nou_binar[idx1]), precizie)
#             valori_noi_x[idx2] = round(decodificare(x, discretizare, sir_nou_binar[idx2]), precizie)
#             valori_noi_functie[idx1] = calculare_valoare_functie(a, b, c, valori_noi_x[idx1])
#             valori_noi_functie[idx2] = calculare_valoare_functie(a, b, c, valori_noi_x[idx2])
#             f.write(f"{sir_nou_binar[idx1]} {sir_nou_binar[idx2]}\n")
#         else:
#             f.write(f"{sir_nou_binar[idx1]} {sir_nou_binar[idx2]}\n")
#
# def mutatie_populatie(dimensiune: int, probabilitate_mutatie: float, sir_nou_binar: List[str],
#                        x: int, discretizare: float, precizie: int, a: int, b: int, c: int, f) -> None:
#     """
#     Efectuează mutația pentru fiecare cromozom: pentru fiecare genă, se verifică
#     dacă se efectuează sau nu mutația, actualizând ulterior valorile cromozomului.
#     """
#     f.write(f"\nProbabilitatea de mutatie pentru fiecare gene: {probabilitate_mutatie / 100}\n")
#     f.write("Au fost modificati cromozomii:\n")
#     for i in range(dimensiune):
#         lista = list(sir_nou_binar[i])
#         for j in range(len(lista)):
#             if random.random() < probabilitate_mutatie / 100:
#                 lista[j] = '1' if lista[j] == '0' else '0'
#                 f.write(f'{i + 1}\n')
#         sir_nou_binar[i] = ''.join(lista)
#     f.write("Dupa mutatie:\n")
#     for i in range(dimensiune):
#         val_x = round(decodificare(x, discretizare, sir_nou_binar[i]), precizie)
#         f.write(f"{i + 1:2d}: {sir_nou_binar[i]} x= {val_x} f= {calculare_valoare_functie(a, b, c, val_x)}\n")
#
# def evaluare_populatie(dimensiune: int, sirBinar: List[str], x: int, discretizare: float, precizie: int,
#                         a: int, b: int, c: int, f) -> Tuple[List[float], List[float]]:
#     """
#     Recalculează valorile x și ale funcției pentru fiecare cromozom din populație.
#     """
#     valori_x = [0.0] * dimensiune
#     valori_functie = [0.0] * dimensiune
#     for i in range(dimensiune):
#         val_x = round(decodificare(x, discretizare, sirBinar[i]), precizie)
#         valori_x[i] = val_x
#         valori_functie[i] = calculare_valoare_functie(a, b, c, val_x)
#     return valori_x, valori_functie
#
# def evolutie_etapa(etapa: int, dimensiune: int, probabilitate_recombinare: float, probabilitate_mutatie: float,
#                     sirBinar: List[str], x: int, discretizare: float, precizie: int,
#                     a: int, b: int, c: int, f) -> Tuple[List[str], List[float], List[float]]:
#     """
#     Realizează o etapă de evoluție: se face selecția, recombinarea și mutația,
#     apoi se evaluează populația și se scrie maximul fitness obținut.
#     """
#     valori_x, valori_functie = evaluare_populatie(dimensiune, sirBinar, x, discretizare, precizie, a, b, c, f)
#     _, q = calcul_probabilitati(valori_functie, f)
#     valori_noi_x, valori_noi_functie, sir_nou_binar = selectie_populatie(dimensiune, q, valori_x, valori_functie, sirBinar, f)
#     recombinare_populatie(dimensiune, probabilitate_recombinare, sir_nou_binar, valori_noi_x, valori_noi_functie,
#                           x, discretizare, precizie, a, b, c, f)
#     mutatie_populatie(dimensiune, probabilitate_mutatie, sir_nou_binar, x, discretizare, precizie, a, b, c, f)
#     valori_noi_x, valori_noi_functie = evaluare_populatie(dimensiune, sir_nou_binar, x, discretizare, precizie, a, b, c, f)
#     f.write(f"Etapa {etapa}: Max fitness = {max(valori_noi_functie)}\n")
#     return sir_nou_binar, valori_noi_x, valori_noi_functie
#
#
# # Funcția principală
#
# def main():
#     # Citirea valorilor de intrare
#     dimensiunePopulatie = int(input("Introduceti dimensiunea populatiei: "))
#     x, y = map(int, input("Introduceti capetele intervalului (x y): ").split())
#     a, b, c = map(int, input("Introduceti parametrii functiei (a b c): ").split())
#     precizie = int(input("Introduceti precizia: "))
#     probabilitate_recombinare = float(input("Introduceti probabilitatea de recombinare: "))
#     probabilitate_mutatie = float(input("Introduceti probabilitatea de mutatie: "))
#     numar_etape = int(input("Introduceti numarul de etape: "))
#
#     # Calcularea discretizării și a valorii L
#     nr = y - x
#     nr = calculate_number(precizie, nr)
#     l = 0
#     l, nr = calculate_l(l, nr)
#     discretizare = (y - x) / float(nr)
#
#     with open("rezultate.txt", 'w') as f:
#         f.write("Populatia initiala:\n")
#         valori_x, sirBinar, valori_functie, suma_totala = initializare_populatie(dimensiunePopulatie, x, y, precizie,
#                                                                                  a, b, c, discretizare, l, f)
#         f.write(f"\nSuma totala a functiilor: {suma_totala}\n")
#         _, q = calcul_probabilitati(valori_functie, f)
#         valori_noi_x, valori_noi_functie, sir_nou_binar = selectie_populatie(dimensiunePopulatie, q, valori_x, valori_functie, sirBinar, f)
#         # Recombinare
#         recombinare_populatie(dimensiunePopulatie, probabilitate_recombinare, sir_nou_binar, valori_noi_x,
#                               valori_noi_functie, x, discretizare, precizie, a, b, c, f)
#         # Mutație
#         mutatie_populatie(dimensiunePopulatie, probabilitate_mutatie, sir_nou_binar, x, discretizare, precizie, a, b, c, f)
#         f.write("\nDupa recombinare si mutatie:\n")
#         valori_noi_x, valori_noi_functie = evaluare_populatie(dimensiunePopulatie, sir_nou_binar, x, discretizare, precizie, a, b, c, f)
#         for i in range(dimensiunePopulatie):
#             f.write(f"{i + 1:2d}: {sir_nou_binar[i]} x= {valori_noi_x[i]} f= {valori_noi_functie[i]}\n")
#         f.write("\nEvolutia maximului:\n")
#         f.write(f"Etapa 1: Max fitness = {max(valori_noi_functie)}\n")
#         # Evoluția pe etape
#         for etapa in range(2, numar_etape + 1):
#             sir_nou_binar, valori_noi_x, valori_noi_functie = evolutie_etapa(etapa, dimensiunePopulatie,
#                                                                              probabilitate_recombinare,
#                                                                              probabilitate_mutatie,
#                                                                              sir_nou_binar, x,
#                                                                              discretizare, precizie,
#                                                                              a, b, c, f)
#
# if __name__ == "__main__":
#     main()

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

# Folosind cautarea binara se gaseste intervalul pentru un numar uniform generat analog unui cromozom
def gasire_interval(x: float, intervale: List[float]) ->  float:
    i = bisect.bisect_right(intervale, x) # Cautarea binara importata direct
    if i == 0 or i >= len(intervale):
        raise ValueError(f"Numărul {x} este în afara intervalelor definite")
    return i

# Primind un numar in binar, ii aflam valorea float
def decodificare(x: float, discretizare: float, sir: str) -> float:
    numar = int(sir, 2)  # Converteste direct din binar în întreg
    max_posibil = (1 << len(sir)) - 1  # Echivalent cu 2^len(sir) - 1
    return x + (numar / max_posibil) * (discretizare * max_posibil)

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

    # Avem cate 2 pentru fiecare deoarece ne va folosi in etapa de selectie

    suma_totala_val_functie = 0.0
    probabilitati_selectie_cromozom = [0.0] * dimensiunePopulatie
    numere_uniforme = [0.0] * dimensiunePopulatie

    # Punem intr-un vector separat numerele care vor participa la recombinare
    numere_recombinare = [""] * dimensiunePopulatie

    # Pentru fiecare numar care participa la recombinare tinem minte index sau in vectorul inital
    index_recombinare = [0] * dimensiunePopulatie

    # Calcularea discretizarii si a valorii L
    nr = y - x
    nr = calculate_number(precizie, nr)
    l = 0
    l, nr = calculate_l(l, nr)
    discretizare = (y - x) / float(nr)

    #Populatia initiala
    with open("rezultate.txt", 'w') as f:
        for i in range(dimensiunePopulatie):
            # Valorea corespunzatoare cromozomului in domeniu de definitie
            valori_x[i] = gen_numar_aleator(x, y, precizie)

            # Reprezentarea pe biti a cromozomului
            sirBinar[i] = generare_sir_binar(x, discretizare, l, valori_x[i])

            # Valorea cromozomului, valorea functiei in punctul din domeniu
            valori_functie[i] = calculare_valoare_functie(a, b, c, valori_x[i])

            # Suma tuturor valorilor functiei
            suma_totala_val_functie += valori_functie[i]
            f.write(f"{i + 1:2d}: {sirBinar[i]} x= {valori_x[i]: } f= {valori_functie[i]:}\n")



        # ------------------------------------------------------------- SELECTIA -------------------------------------------------------------



        f.write("\n")
        f.write("Probabilitati selectie:\n")

        #Probabilitatea de selectie pentru fiecare cromozom
        for i in range(dimensiunePopulatie):
            probabilitati_selectie_cromozom[i] = valori_functie[i] / suma_totala_val_functie
            f.write(f"cromozom  {i + 1:2d} probabilitate {probabilitati_selectie_cromozom[i]}\n")

        # Suma tuturor valorilor functiei
        f.write("\n")
        f.write("Suma totala:")
        f.write(f"{suma_totala_val_functie}\n")

        f.write("\n")
        f.write('Intervale probabilitati de selectie:\n')
        q = [0.0] * (dimensiunePopulatie + 1)
        q[0] = 0.0
        f.write(f'0.0\n')

        # Calculam si afisam intervalele de selectie
        for i in range(1, dimensiunePopulatie + 1):
            temp = q[i - 1]
            q[i] = temp + probabilitati_selectie_cromozom[i - 1]
            f.write(f'{q[i]}\n')

        # Generam numerele uniforme pentru a vedea care cromozomi sunt selectati in urmatoarea populatie
        f.write("\n")
        f.write('Nunerele uniforme: \n')
        for i in range(dimensiunePopulatie):
            numere_uniforme[i] = random.random() # Genereaza un numar din intervalul [0, 1)
            f.write(f"u = {numere_uniforme[i]:8} \t selectat cromozomul {gasire_interval(numere_uniforme[i], q):2d}\n")
            index = gasire_interval(numere_uniforme[i], q) - 1
            valori_noi_x[i] = valori_x[int(index)] # Punem in noul vector noua populatie selectata
            valori_noi_functie[i] = valori_functie[int(index)]
            sir_nou_binar[i] = sirBinar[int(index)]

        # Afisam noua populatie dupa pasul de selectie
        f.write("\n")
        f.write('Dupa selectie: \n')
        for i in range(dimensiunePopulatie):
            f.write(f"{i + 1:2d}: {sir_nou_binar[i]} x= {valori_noi_x[i]: } f= {valori_noi_functie[i]:}\n")



        # ------------------------------------------------------------- INCRUCISAREA -------------------------------------------------------------



        lungimeRecombinare = 0
        f.write('\n')
        f.write(f"Probabilitate de incrucisare: {probabilitate_recombinare}\n")
        for i in range(dimensiunePopulatie):
            numere_uniforme[i] = random.random() # Generam un numar aleatoriu din intervalul [0, 1)
            if numere_uniforme[i] < probabilitate_recombinare / 100:
                # Daca numarul generat pentru cromozomul i este mai mic decat probabilitatea de recombinare
                # Il adaugam in noul vector numere_recombinare si ii tinem minte indexul in vectorul original de valori
                f.write(f'{i + 1}: {sir_nou_binar[i]} u= {numere_uniforme[i]} < {probabilitate_recombinare} participa\n')
                numere_recombinare[lungimeRecombinare] = sir_nou_binar[i]
                index_recombinare[lungimeRecombinare] = i
                lungimeRecombinare += 1
            else:
                f.write(f'{i + 1}: {sir_nou_binar[i]} u= {numere_uniforme[i]}\n')

        # Daca avem numar impar de numere care participa la recombinare, il putem ignora pe ultimul
        if lungimeRecombinare % 2 != 0:
            numere_recombinare[lungimeRecombinare] = ""
            lungimeRecombinare -= 1

        # Afisam procesul de recombinare
        f.write('\nProcesul de recombinare: \n')
        for i in range(0, lungimeRecombinare, 2):
            # Vom parcurge cromozomii care iau parte la recombinare 2 cate 2
            f.write(f'Recombinare dintre cromozomul {index_recombinare[i] + 1} cu cromozomul {index_recombinare[i+1] + 1}:\n')
            f.write(f'{numere_recombinare[i]} ')
            f.write(f'{numere_recombinare[i+1]} ')
            # Generam punctul de incrucisare pentru cei 2 cromozomi
            # Un numar aleator intre 0 si lungimea maxima a unui numar in binar
            punct = random.randint(0, len(sir_nou_binar[0]))
            f.write(f'punct {punct}\n')
            f.write('Rezulat: \n')
            # Daca punctul generat este egal cu 0 nu este nevoie sa schimbam cromozomii
            if punct == 0:
                f.write(f'{numere_recombinare[i]} ')
                f.write(f'{numere_recombinare[i+1]}\n')
            else:
                for j in range(punct, len(sir_nou_binar[0])):

                    lista_i = list(numere_recombinare[i])
                    lista_i_plus_1 = list(numere_recombinare[i+1])

                    # Interschimbam fiecare "bit" incepand de la punctul generat pana la finarul sirului binar
                    temp = lista_i[j]
                    lista_i[j] = lista_i_plus_1[j]
                    lista_i_plus_1[j] = temp

                    numere_recombinare[i] = ''.join(lista_i)
                    numere_recombinare[i+1] = ''.join(lista_i_plus_1)

                sir_nou_binar[index_recombinare[i]] = numere_recombinare[i]
                sir_nou_binar[index_recombinare[i+1]] = numere_recombinare[i+1]
                valori_noi_x[index_recombinare[i]] = round(decodificare(x, discretizare, sir_nou_binar[index_recombinare[i]]), precizie)
                valori_noi_x[index_recombinare[i+1]] = round(decodificare(x, discretizare, sir_nou_binar[index_recombinare[i+1]]), precizie)
                valori_noi_functie[index_recombinare[i]] = calculare_valoare_functie(a, b, c, valori_noi_x[index_recombinare[i]])
                valori_noi_functie[index_recombinare[i+1]] = calculare_valoare_functie(a, b, c, valori_noi_x[index_recombinare[i+1]])

                f.write(f'{sir_nou_binar[index_recombinare[i]]} ')
                f.write(f'{sir_nou_binar[index_recombinare[i+1]]}\n')

        f.write('\n Dupa recombinare: \n')
        for i in range(dimensiunePopulatie):
            f.write(f"{i + 1:2d}: {sir_nou_binar[i]} x= {valori_noi_x[i]: } f= {valori_noi_functie[i]:}\n")




        # ------------------------------------------------------------- MUTATIE -------------------------------------------------------------




        f.write(f'\nProbabilitatea de mutatie pentru fiecare gene {probabilitate_mutatie / 100}\n')
        f.write('Au fost modificati cromozomii: \n')
        for i in range(dimensiunePopulatie):
            for j in range(len(sir_nou_binar[i])):
                # Pentru fiecare "bit" dintr-un sir binar, generam un numar aleator intre [0, 1)
                # Iar daca este mai mic decat probabilitatea de mutatie, interschimbam "bit-ul"
                numar_uniform = random.random()
                lista_i = list(sir_nou_binar[i])
                if(numar_uniform < probabilitate_mutatie / 100):
                    if(lista_i[j] == '0'):
                        lista_i[j] = '1'
                    else:
                        lista_i[j] = '0'
                    f.write(f'{i + 1}\n')
                sir_nou_binar[i] = ''.join(lista_i)
                valori_noi_x[i] = round(decodificare(x, discretizare, sir_nou_binar[i]), precizie)
                valori_noi_functie[i] = calculare_valoare_functie(a, b, c, valori_noi_x[i])

        f.write('Dupa mutatie: \n')
        for i in range(dimensiunePopulatie):
            f.write(f"{i + 1:2d}: {sir_nou_binar[i]} x= {valori_noi_x[i]: } f= {valori_noi_functie[i]:}\n")

        f.write('\nEvolutia maximului: \n')
        f.write(f"Etapa 1: Max fitness = {max(valori_noi_functie)}\n")




        # ------------------------------------------------------------- ETAPELE -------------------------------------------------------------




        for etapa in range(2, numar_etape + 1):
            suma_totala_val_functie = 0.0

            probabilitati_selectie_cromozom = [val / sum(valori_noi_functie) for val in valori_noi_functie]
            q = [0.0] * (dimensiunePopulatie + 1)
            for i in range(1, dimensiunePopulatie + 1):
                q[i] = q[i - 1] + probabilitati_selectie_cromozom[i - 1]

            for i in range(dimensiunePopulatie):
                numere_uniforme[i] = random.random()
                index = gasire_interval(numere_uniforme[i], q) - 1
                valori_x[i] = valori_noi_x[int(index)]
                valori_functie[i] = valori_noi_functie[int(index)]
                sirBinar[i] = sir_nou_binar[int(index)]

            # Recombinare
            index_recombinare = []
            for i in range(dimensiunePopulatie):
                if random.random() < probabilitate_recombinare / 100:
                    index_recombinare.append(i)

            if len(index_recombinare) % 2 != 0:
                index_recombinare.pop()

            for i in range(0, len(index_recombinare), 2):
                idx1 = index_recombinare[i]
                idx2 = index_recombinare[i + 1]
                punct = random.randint(0, len(sirBinar[0]))
                crom1 = list(sirBinar[idx1])
                crom2 = list(sirBinar[idx2])

                for j in range(punct, len(crom1)):
                    crom1[j], crom2[j] = crom2[j], crom1[j]

                sirBinar[idx1] = ''.join(crom1)
                sirBinar[idx2] = ''.join(crom2)

            # Mutatie
            for i in range(dimensiunePopulatie):
                gene = list(sirBinar[i])
                for j in range(len(gene)):
                    if random.random() < probabilitate_mutatie / 100:
                        gene[j] = '1' if gene[j] == '0' else '0'
                sirBinar[i] = ''.join(gene)

            # Evaluare noua populatie
            for i in range(dimensiunePopulatie):
                valori_noi_x[i] = round(decodificare(x, discretizare, sirBinar[i]), precizie)
                valori_noi_functie[i] = calculare_valoare_functie(a, b, c, valori_noi_x[i])

            # Salvare maxim
            max_fitness = max(valori_noi_functie)
            f.write(f"Etapa {etapa}: Max fitness = {max_fitness}\n")


if __name__ == "__main__":
    main()



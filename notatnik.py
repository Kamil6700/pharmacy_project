# napisz funkcje która będzie obliczała pole koła o promieniu podanym przez użytkwnika
import math
def pole_kola(promien):
    return math.pi*promien**2
promien = float(input("Podaj długość promienia: "))
print(pole_kola(promien))

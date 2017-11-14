"""FUNÇÃO GLOBAL
Código exemplo de utilização da biblioteca "adc8"
"""
#!/usr/bin/python
from lib.dado import Dado
from lib.datilografo import Escritor
from lib.adc8 import ADC8
import time

# Cria objeto Escritor
escritor = Escritor("   ", True, True, "ADC8 - ", ".csv")

# Cria objeto do ADC
adc8 = ADC8()

# Cria alguns dados do adc
item = Dado("Item", "it", "itn", True, True, False)
tempo = Dado("Tempo", "Segundos", "tmp", True, True, False)
analog0 = Dado("a0", "anolog", "awd", True, True, True)
analog1 = Dado("Rotação do motor", "Rpm", "rpm", True, True, False)
analog2 = Dado("Posição X GPS", "Metros", "pox", True, False, False)
analog3 = Dado("Pitot", "awdaw", "aaa", True, True, True)

inicio = int(round(time.time() * 1000))


def atualizaEscritor():
    """Atualiza vetor de dados e passa eles para o Escritor
    """
    d = [item, tempo, analog0, analog1, analog2, analog3]
    escritor.setDados(d)


# Faz cabeçalho
atualizaEscritor()
escritor.fazCabecalho()
tempoAgora = int(round(time.time() * 1000)) - inicio
item.setValor(0)

# Faz iterações de escritas de linha, modificando os valore dos dados
for x in range(1000):
    analog0.setValor(adc8.getCanal0())
    analog1.setValor(adc8.getCanal1())
    analog2.setValor(adc8.getCanal2())
    analog3.setValor(adc8.getCanal3())
    item.setValor(item.getValor() + 1)
    tempoAgora = int(round(time.time() * 1000)) - inicio
    tempo.setValor(tempoAgora)
    print(analog0.getValor(), ", ", analog1.getValor(),
          ", ", analog2.getValor(), ", ", analog3.getValor())
    atualizaEscritor()
    escritor.escreveLinhaDado()

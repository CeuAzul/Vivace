"""FUNÇÃO GLOBAL
Código exemplo de utilização da biblioteca de conexão com nano
"""
#!/usr/bin/python
import time
from lib.dado import Dado
from lib.datilografo import Escritor
from lib.nanolib import Nano

# Cria objeto do transmissor
nano = Nano()

# Cria objeto Escritor
escritor = Escritor(",", True, True, "Fred - ", ".csv")


# Cria objetos dos Dados
tempo = Dado("Tempo", "Segundos", "tmp", True, True, True)
cor1 = Dado("Corrente1", "A", "cru", True, True, False)
cor2 = Dado("Corrente2", "A", "crd", True, True, False)
cor3 = Dado("Corrente3", "A", "crt", True, True, False)
voltBat = Dado("Tensão Bateria", "V", "vtb", True, False, False)
pwm1 = Dado("PWM1", "Microssec", "pwu", True, False, False)
pwm2 = Dado("PWM2", "Microssec", "pwd", True, False, False)
pwm3 = Dado("PWM3", "Microssec", "pwt", True, False, False)

inicio = int(round(time.time() * 1000))


def atualizaEscritor():
    """Atualiza vetor de dados e passa eles para o Escritor
    """
    d = [tempo, cor1, cor2, cor3, voltBat, pwm1, pwm2, pwm3]
    escritor.setDados(d)


# Faz cabeçalho
atualizaEscritor()
escritor.fazCabecalho()
tempoAgora = int(round(time.time() * 1000)) - inicio

# Faz iterações de escritas de linha, modificando os valore dos dados
for x in range(1000):
    nano.atualiza()
    cor1.setValor(nano.getRpmD())
    cor2.setValor(nano.getRpmE())
    cor3.setValor(nano.getWow())
    voltBat.setValor(nano.getWowRaw())
    pwm1.setValor(nano.getTempoVoo())
    pwm2.setValor(nano.getDistancia())
    pwm3.setValor(nano.getDistRef())
    tempoAgora = int(round(time.time() * 1000)) - inicio
    tempo.setValor(tempoAgora)
    print(cor1.getValor(), ", ", cor2.getValor(), ", ", cor3.getValor(), ", ", voltBat.getValor(
    ), ", ", pwm1.getValor(), ", ", pwm2.getValor(), ", ", pwm3.getValor())
    atualizaEscritor()
    escritor.escreveLinhaDado()
    time.sleep(0.2)

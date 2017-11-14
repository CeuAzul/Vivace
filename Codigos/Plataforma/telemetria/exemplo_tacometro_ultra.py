"""FUNÇÃO GLOBAL
Código exemplo de utilização da biblioteca de conexão com nano
"""
#!/usr/bin/python
import time
from lib.dado import Dado
from lib.datilografo import Escritor
from lib.nanolib import Nano

#Cria objeto do transmissor
nano = Nano()

#Cria objeto Escritor
escritor = Escritor(",", True, True, "Tacosom - ", ".csv")


#Cria objetos dos Dados
tempo = Dado("Tempo", "Segundos", "tmp", True, True, True)
rpmD = Dado("Rotacao do motor Direita", "Rpm", "rpm", True, True, False)
rpmE = Dado("Rotacao do motor Esquerda", "Rpd", "rpm", True, True, False)
wow = Dado("Wow", "bit", "wow", True, True, False)
wowRaw = Dado("Wow raw", "bit", "wop", True, False, False)
tempoVoo = Dado("Tempo de voo", "s", "tpv", True, False, False)
distancia = Dado("Distância", "cm", "tpv", True, False, False)
distRef = Dado("Distancia referência", "cm", "dsr", True, False, False)

inicio = int(round(time.time()*1000))

def atualizaEscritor():
    """Atualiza vetor de dados e passa eles para o Escritor
    """
    d = [tempo, rpmD, rpmE, wow, wowRaw, tempoVoo, distancia, distRef]
    escritor.setDados(d)


#Faz cabeçalho
atualizaEscritor()
escritor.fazCabecalho()
tempoAgora = int(round(time.time()*1000)) - inicio

#Faz iterações de escritas de linha, modificando os valore dos dados
for x in range(1000):
    nano.atualiza()
    rpmD.setValor(nano.getRpmD())
    rpmE.setValor(nano.getRpmE())
    wow.setValor(nano.getWow())
    wowRaw.setValor(nano.getWowRaw())
    tempoVoo.setValor(nano.getTempoVoo())
    distancia.setValor(nano.getDistancia())
    distRef.setValor(nano.getDistRef())
    tempoAgora = int(round(time.time()*1000)) - inicio
    tempo.setValor(tempoAgora)
    print(wow.getValor(),", ", rpmD.getValor(),", ", rpmE.getValor(),", ", wowRaw.getValor(),", ", tempoVoo.getValor(),", ", distancia.getValor(),", ",distRef.getValor())
    atualizaEscritor()
    escritor.escreveLinhaDado()
    time.sleep(0.4)


        
            

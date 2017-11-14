"""FUNÇÃO GLOBAL
Código exemplo de utilização da biblioteca de transmissão de dados
"""
#!/usr/bin/python
import time
import os
from lib.dado import Dado
from lib.telepatia import Transmissor

#Cria objeto do transmissor
transmissor = Transmissor("   ", True, 57600, 'UTF-8')

#Cria objetos dos Dados
tempo = Dado("Tempo", "Segundos", "tmp", True, True, True)
rpm = Dado("Rotacao do motor", "Rpm", "rpm", True, True, False)
hp = Dado("hp", "pes", "hps", True, True, False)
velca = Dado("Velocidade calibrada", "m/s", "vel", True, True, False)
posicaoX = Dado("Posicao X GPS", "Metros", "pox", True, True, False)
posicaoY = Dado("Posicao Y GPS", "Metros", "poy", True, True, False)
posicaoZ = Dado("Posicao Z GPS", "Metros", "poz",  True, True, False)

inicio = int(round(time.time()*1000))
def atualizaTransmissor():
    """Função atualiza vetor de Dados e atualiza o transmissor
    """
    d = [tempo, rpm, hp, velca, posicaoX, posicaoY, posicaoZ]
    transmissor.setDados(d)


atualizaTransmissor()

#Código periódico que coloca valores aleatórios e transmite-os
while True:
    receb = transmissor.leLinha()
    if (receb):
        print(receb)
        if (receb == "vai"):
            print("foi")
            for x in range(1000):
                ddt = int(round(time.time()*1000)) - inicio
                tempo.setValor(ddt)
                rpm.setValor(1000+x)
                hp.setValor(2*x)
                velca.setValor(2*100*x+x)
                posicaoX.setValor(200+x)
                posicaoY.setValor(200*x)
                posicaoZ.setValor(4*x)
                atualizaTransmissor()
                transmissor.transmiteLinha()
                #print("oi")
                time.sleep(0.1)
        if (receb =="reinicia"):
            os.system('sudo reboot')
        if (receb =="desliga"):
            os.system('sudo shutdown now')
    time.sleep(1)


        
            

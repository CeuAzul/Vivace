#!/usr/bin/python
# -*- coding: utf-8 -*-

"""FUNÇÃO GLOBAL
Código que cria objeto de todos os sensore e faz com que eles
trabalhem em harmonia usando as threads.
"""

import time
import os
from datetime import datetime
import threading

from ajudante import Ajudante
from ajudante import Thredeiro
from configurador import Configurador

def main():

    ajudante = Ajudante()

    ajudante.ativar_sensores()
    ajudante.criar_dados()
    ajudante.ativar_gravacao()
    ajudante.ativar_transmissao()
    ajudante.criar_escritor_transmissor()
    ajudante.trocarModoDeTransmissao(0)
    ajudante.escritor.setDados(ajudante.receber_pacote_de_dados)
    #ajudante.escritor.fazCabecalho()


    while ajudante.threadsRodando == True:
        threadTransmissao = Thredeiro(ajudante.transmitirDados, 0.5)
        threadIMU = Thredeiro(ajudante.atualizarIMU, 0.03)
        threadBARO = Thredeiro(ajudante.atualizarBarometro, 0.1)
        threadGPS = Thredeiro(ajudante.atualizarGps, 0.5)
        threadPITOT = Thredeiro(ajudante.atualizarPitot, 0.2)
        threadNANO = Thredeiro(ajudante.atualizarNano, 0.5)
        threadGravacao = Thredeiro(ajudante.gravarDados, 0.02)
        threadTelecomando = Thredeiro(ajudante.lerTelecomando, 1)


if __name__ == '__main__':

    main()

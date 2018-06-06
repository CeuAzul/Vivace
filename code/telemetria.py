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

    threadTransmissao = Thredeiro('Transmissao', ajudante.transmitirDados, 0.5)
    threadIMU = Thredeiro('IMU', ajudante.atualizarIMU, 0.03)
    threadBARO = Thredeiro('BARO', ajudante.atualizarBarometro, 0.1)
    threadGPS = Thredeiro('GPS', ajudante.atualizarGps, 0.5)
    threadPITOT = Thredeiro('PITOT', ajudante.atualizarPitot, 0.2)
    threadNANO = Thredeiro('NANO', ajudante.atualizarNano, 0.5)
    threadGravacao = Thredeiro('Gravaçao', ajudante.gravarDados, 0.02)
    threadTelecomando = Thredeiro('Telecomando', ajudante.lerTelecomando, 1)


if __name__ == '__main__':

    main()

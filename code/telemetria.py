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

    configurador = Configurador()

    ajudante = Ajudante(configurador)

    ajudante.ativar_sensores()
    ajudante.criar_dados()
    ajudante.ativar_gravacao()
    ajudante.ativar_transmissao()
    ajudante.criar_escritor_transmissor()
    ajudante.trocarModoDeTransmissao(4)
    ajudante.escritor.setDados(ajudante.receber_pacote_de_dados())
    ajudante.escritor.fazCabecalho()

    if(configurador.ATIVAR_TRANSMISSAO):
        threadTransmissao = Thredeiro('Transmissao', ajudante.transmitirDados, 0.5)
    if(configurador.USAR_IMU):
        threadIMU = Thredeiro('IMU', ajudante.atualizarIMU, 0.03)
    if(configurador.USAR_BARO):
        threadBARO = Thredeiro('BARO', ajudante.atualizarBarometro, 0.1)
    if(configurador.USAR_GPS):
        threadGPS = Thredeiro('GPS', ajudante.atualizarGps, 0.5)
    if(configurador.USAR_PITOTS):
        threadPITOT = Thredeiro('PITOT', ajudante.atualizarPitot, 0.2)
    if(configurador.USAR_BALANCA):
        threadBALANCA = Thredeiro('BALANCA', ajudante.atualizarBalanca, 0.05)
    if(configurador.USAR_CELULAS):
        threadCELULAS = Thredeiro('CELULAS', ajudante.atualizarCelulas, 0.05)
    if(configurador.USAR_ARDUINO):
        threadARDUINO = Thredeiro('ARDUINO', ajudante.atualizarArduino, 0.05)
    if(configurador.ATIVAR_GRAVACAO):
        threadGravacao = Thredeiro('Gravaçao', ajudante.gravarDados, 0.02)
    if(configurador.ATIVAR_TRANSMISSAO):
        threadTelecomando = Thredeiro('Telecomando', ajudante.lerTelecomando, 1)


if __name__ == '__main__':

    main()

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
import sys

from ajudante import Ajudante
from thredeiro import Thredeiro
from configurador import Configurador
from atualizador import Atualizador
from criador import Criador

def main():

    configurador = Configurador()
    criador = Criador(configurador)
    ajudante = Ajudante(configurador, criador)
    atualizador = Atualizador(configurador, criador, ajudante)

    criador.criar_sensores()
    criador.criar_dados()
    criador.criar_escritor()
    criador.criar_transmissor()
    if configurador.ATIVAR_GRAVACAO:
        criador.escritor.setDados(ajudante.receber_dados_usados())
        criador.escritor.fazCabecalho()

    if(configurador.ATIVAR_TRANSMISSAO):
        threadTransmissao = Thredeiro('Transmissao', ajudante.transmitirDados, 0.5)
    if(configurador.USAR_IMU):
        threadIMU = Thredeiro('IMU', atualizador.atualizarIMU, 0.03)
    if(configurador.USAR_BARO):
        threadBARO = Thredeiro('BARO', atualizador.atualizarBarometro, 0.1)
    if(configurador.USAR_GPS):
        threadGPS = Thredeiro('GPS', atualizador.atualizarGps, 0.5)
    if(configurador.USAR_PITOTS):
        threadPITOT = Thredeiro('PITOT', atualizador.atualizarPitot, 0.2)
    if(configurador.USAR_BALANCA):
        threadBALANCA = Thredeiro('BALANCA', atualizador.atualizarBalanca, 0.05)
    if(configurador.USAR_CELULAS):
        threadCELULAS = Thredeiro('CELULAS', atualizador.atualizarCelulas, 0.05)
    if(configurador.USAR_ARDUINO):
        threadARDUINO = Thredeiro('ARDUINO', atualizador.atualizarArduino, 0.05)
    if(configurador.ATIVAR_GRAVACAO):
        threadGravacao = Thredeiro('Gravaçao', ajudante.gravarDados, 0.02)
    if(configurador.ATIVAR_TRANSMISSAO):
        threadTelecomando = Thredeiro('Telecomando', ajudante.lerTelecomando, 1)


if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        print('Program interrupted')
        sys.exit()
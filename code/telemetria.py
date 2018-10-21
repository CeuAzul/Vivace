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

from modos_de_transmissao import SeletorDeModos

def main():

    configurador = Configurador()
    criador = Criador(configurador)
    seletor = SeletorDeModos(criador)
    ajudante = Ajudante(configurador, criador, seletor)
    atualizador = Atualizador(configurador, criador, ajudante)

    criador.criar_transmissor()
    criador.criar_dados_gerais()
    if(configurador.ENVIAR_SINAL_DE_VIDA):
        threadDaVida = Thredeiro('SinaldeVida', atualizador.enviarSinalDeVida, 0.1)
    if(configurador.ATIVAR_TRANSMISSAO):
        threadTelecomando = Thredeiro('Telecomando', atualizador.lerTelecomando, 0.5)
    else:
        ajudante.configuracoes_recebidas = True

    while ajudante.configuracoes_recebidas == False:
        pass

    criador.criar_escritor()
    criador.criar_sensores()
    criador.criar_dados_sensores()

    if configurador.ATIVAR_GRAVACAO:
        criador.escritor.setDados(ajudante.receber_dados_usados())
        criador.escritor.fazCabecalho()
    if configurador.ATIVAR_TRANSMISSAO:
        if(configurador.TRANSMITIR_IMU):
            ajudante.ativar_transmissao('IMU')
        if(configurador.TRANSMITIR_BARO):
            ajudante.ativar_transmissao('BARO')
        if(configurador.TRANSMITIR_GPS):
            ajudante.ativar_transmissao('GPS')
        if(configurador.TRANSMITIR_PITOTS):
            ajudante.ativar_transmissao('PITOT')
        if(configurador.TRANSMITIR_SONDAS_AOA):
            ajudante.ativar_transmissao('SONDA_AOA')
        if(configurador.TRANSMITIR_CELULAS):
            ajudante.ativar_transmissao('CELULA')
    seletor.setModo(4)

    threadGeral = Thredeiro('Dados gerais', atualizador.atualizarGeral, 0.01)

    if(configurador.USAR_IMU):
        threadIMU = Thredeiro('IMU', atualizador.atualizarIMU, 0.02)
    if(configurador.USAR_BARO):
        threadBARO = Thredeiro('BARO', atualizador.atualizarBarometro, 0.1)
    if(configurador.USAR_GPS):
        threadGPS = Thredeiro('GPS', atualizador.atualizarGps, 0.5)
    if(configurador.USAR_PITOTS):
        threadPITOT = Thredeiro('PITOT', atualizador.atualizarPitot, 0.01)
    if(configurador.USAR_SONDAS_AOA):
        threadPITOT = Thredeiro('SONDA_AOA', atualizador.atualizarSondasAoA, 0.01)
    if(configurador.USAR_BALANCA):
        threadBALANCA = Thredeiro('BALANCA', atualizador.atualizarBalanca, 0.01)
    if(configurador.USAR_CELULAS):
        threadCELULAS = Thredeiro('CELULAS', atualizador.atualizarCelulas, 0.01)
    if(configurador.USAR_ARDUINO):
        threadARDUINO = Thredeiro('ARDUINO', atualizador.atualizarArduino, 0.01)
    if(configurador.ATIVAR_TRANSMISSAO):
        threadTransmissao = Thredeiro('Transmissao', atualizador.transmitirDados, 0.1)
    if(configurador.ATIVAR_GRAVACAO):
        threadGravacao = Thredeiro('Gravaçao', atualizador.gravarDados, 0.005)

if __name__ == '__main__':
    main()

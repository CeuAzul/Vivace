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
        criador.escritor.dados = criador.receber_todos_os_dados()
        criador.escritor.fazCabecalho()
    if configurador.ATIVAR_TRANSMISSAO:
        for sensor in configurador.LISTA_TRANSMITIR:
            ajudante.ativar_transmissao(sensor)
    seletor.setModo(4)

    threadGeral = Thredeiro('Dados gerais', atualizador.atualizarGeral, 0.01)

    if('IMU' in configurador.LISTA_USAR):
        threadIMU = Thredeiro('IMU', atualizador.atualizarIMU, 0.02)
    if('BARO' in configurador.LISTA_USAR):
        threadBARO = Thredeiro('BARO', atualizador.atualizarBarometro, 0.1)
    if('GPS' in configurador.LISTA_USAR):
        threadGPS = Thredeiro('GPS', atualizador.atualizarGps, 0.5)
    if('PITOT' in configurador.LISTA_USAR):
        threadPITOT = Thredeiro('PITOT', atualizador.atualizarPitot, 0.02)
    if('SONDA_AOA' in configurador.LISTA_USAR):
        threadPITOT = Thredeiro('SONDA_AOA', atualizador.atualizarSondasAoA, 0.02)
    if('BALANCA' in configurador.LISTA_USAR):
        threadBALANCA = Thredeiro('BALANCA', atualizador.atualizarBalanca, 0.05)
    if('CELULA' in configurador.LISTA_USAR):
        threadCELULAS = Thredeiro('CELULAS', atualizador.atualizarCelulas, 0.05)
    if('ARDUINO' in configurador.LISTA_USAR):
        threadARDUINO = Thredeiro('ARDUINO', atualizador.atualizarArduino, 0.01)
    if(configurador.ATIVAR_TRANSMISSAO):
        threadTransmissao = Thredeiro('Transmissao', atualizador.transmitirDados, 0.05)
    if(configurador.ATIVAR_GRAVACAO):
        threadGravacao = Thredeiro('Gravaçao', atualizador.gravarDados, 0.005)

if __name__ == '__main__':
    main()

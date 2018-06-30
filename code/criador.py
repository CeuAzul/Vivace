#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
from datetime import datetime

from libs.dado import Dado

from libs.mpu import MPU
from libs.barometro import Barometro
from libs.gps import GPS
from libs.pitot import Pitot
from libs.arduino import Arduino

from libs.celula import Celula
from libs.balanca import Balanca

from configurador import Configurador

class Criador(object):

    def __init__(self, configurador):
        self.configurador = configurador

    def criar_sensores(self):

        if self.configurador.USAR_ARDUINO:
            try:
                self.arduino = Arduino()
                print('ARDUINO ativado!')
            except:
                self.configurador.USAR_ARDUINO = False
                print('Arduino nao ativado!')

        if self.configurador.USAR_IMU:
            try:
                self.mpu = MPU(True, True, True, True, True, True, True, True)
                print('IMU ativada!')
            except:
                self.configurador.USAR_IMU = False
                print('IMU nao ativada')

        if self.configurador.USAR_BARO:
            try:
                self.barometro = Barometro(True, True)
                print('BARO ativado!')
            except:
                self.configurador.USAR_BARO = False
                print('BARO nao ativado!')

        if self.configurador.USAR_GPS:
            try:
                self.gps = GPS()
                print('GPS ativado!')
            except:
                self.configurador.USAR_GPS = False
                print('GPS nao ativado!')

        if self.configurador.USAR_PITOTS:
            try:
                self.pitots = []
                for i in range(self.configurador.NUMERO_DE_PITOTS):
                    self.pitots.append(Pitot(self.configurador.NOME_DOS_PITOTS[i],
                                                self.configurador.APELIDO_DOS_PITOTS[i],
                                                self.arduino))
                print('PITOTS ativados!')
            except:
                self.configurador.USAR_PITOTS = False
                print('PITOTS nao ativados!')

        if self.configurador.USAR_CELULAS:
            try:
                self.balanca = Balanca()
                self.celulas = []
                for i in range(self.configurador.NUMERO_DE_CELULAS):
                    self.celulas.append(Celula(self.configurador.NOME_DAS_CELULAS[i],
                                                self.configurador.APELIDO_DAS_CELULAS[i],
                                                self.arduino))
                print('CELULAS ativadas!')
            except:
                self.configurador.USAR_CELULAS = False
                self.configurador.USAR_BALANCA = False
                print('CELULAS nao ativadas!')

    def criar_dados(self):

        print('Dados gerais criados')

        self.tempo = Dado("Tempo", "seg", "tmp", True, True, False, 4)
        self.mensagemRecebida = Dado("Mensagem", "str", "str", True, False, False)
        self.modo = Dado("Modo", "int", "sin", False, True, True)
        self.tamanho = Dado("Tamanho do arquivo", "int", "agr", False, True, True, 3)

        print('Dados da IMU criados!')

        self.taxaGiroX = Dado("Taxa de giro em X", "º/s", "gyx", True, False, False, 2, "IMU")
        self.taxaGiroY = Dado("Taxa de giro em Y", "º/s", "gyy", True, False, False, 2, "IMU")
        self.taxaGiroZ = Dado("Taxa de giro em Z", "º/s", "gyz", True, False, False, 2, "IMU")
        self.aceleracaoX = Dado("Aceleração em X", "g", "acx", True, False, False, 2, "IMU")
        self.aceleracaoY = Dado("Aceleração em Y", "g", "acy", True, False, False, 2, "IMU")
        self.aceleracaoZ = Dado("Aceleração em Z", "g", "acz", True, False, False, 2, "IMU")
        self.pitch = Dado("Pitch", "º", "pit", True, False, False, 2, "IMU")
        self.roll = Dado("Roll", "º", "rol", True, False, False, 2, "IMU")

        print('Dados do BARO criados!')

        self.pressaoTotal = Dado("Pressao total", "PA", "ptt", True, True, False, 3, "BARO")
        self.pressaoEstatica = Dado("Pressao estática", "PA", "pts", True, True, False, 3, "BARO")
        self.pressaoTotalr = Dado("PTtotal", "PA", "ptt", True, False, False, 3, "BARO")
        self.pressaoEstaticar = Dado("PTstatic", "PA", "psr", True, False, False, 3, "BARO")
        self.temperaturaBar = Dado("Temperatura", "ºC", "tem", True, False, False, 3, "BARO")
        self.densidadeAr = Dado("Densidade do ar", "Kg/m³", "den", True, False, False, 3, "BARO")
        self.altitudeRelativa = Dado("Altitude relativa", "m", "alt", True, False, False, 3, "BARO")
        self.altitudePressao = Dado("HP", "ft", "hps", True, True, False, 3, "BARO")

        print('Dados do GPS criados!')

        self.dadoTempoGPS = Dado("Tempo GPS", "-", "tmg", True, False, False, "GPS")
        self.latitude = Dado("Latitude", "º", "lat", True, False, False, 6, "GPS")
        self.longitude = Dado("Longitude", "º", "lng", True, False, False, 6, "GPS")
        self.altitude = Dado("ZGPS", "m", "atg", True, False, False, 2, "GPS")
        self.direcaoCurso = Dado("Direção de curso", "º", "cog", True, False, False, 1, "GPS")
        self.velocidade = Dado("Velocidade GPS", "m/s", "vel", True, True, False, 2, "GPS")
        self.velocidadeSubida = Dado("Velocidade de subida", "m/s","ves", False, False, False, 2, "GPS")
        self.erroX = Dado("Erro em X", "m", "erx", False, False, False, 1, "GPS")
        self.erroY = Dado("Erro em Y", "m", "ery", False, False, False, 1, "GPS")
        self.erroAltitude = Dado("Erro da altitude", "m", "era", False, False, False, 1, "GPS")
        self.erroVelocidade = Dado("Erro de velocidade", "nós", "ers", False, False, False, 1, "GPS")
        self.erroVelocidadeSubida = Dado("Erro da velocidade de subida", "m/s", "ves", False, False, False, 1, "GPS")
        self.nivelFixacao = Dado("Nivel de fixação GPS", "-", "nfx", True, False, False, 1, "GPS")
        self.latitudeRef = Dado("Latitude de referência", "-", "ltr", False, True, False, 6, "GPS")
        self.longitudeRef = Dado("Longitude de referência", "-", "lgr", False, True, False, 6, "GPS")
        self.posicaoX = Dado("XGPS", "m", "gpx", True, True, False, 2, "GPS")
        self.posicaoY = Dado("YGPS", "m", "gpy", True, True, False, 2, "GPS")
        self.distanciaAbsoluta = Dado("Distancia absoluta", "m", "dtr", False, False, False, 2, "GPS")

        print('Dados dos PITOTS criados!')

        nomeDosPitots = self.configurador.NOME_DOS_PITOTS
        apelidoDosPitots = self.configurador.APELIDO_DOS_PITOTS

        self.pressaoDin = []
        self.velCas = []

        for pitot in range(self.configurador.NUMERO_DE_PITOTS):
            print(nomeDosPitots[pitot] + ' criado!')
            self.pressaoDin.extend([Dado("Pressao Dinamica - " + nomeDosPitots[pitot], "PA", apelidoDosPitots[pitot], True, True, False, 3, "PITOT")])
            self.velCas.extend([Dado("VCAS - " + nomeDosPitots[pitot], "m/s", "vcs_" + apelidoDosPitots[pitot], True, True, True, 4, "PITOT")])

        print('Dados das CELULAS criados!')

        nomeDasCelulas = self.configurador.NOME_DAS_CELULAS
        apelidoDasCelulas = self.configurador.APELIDO_DAS_CELULAS

        self.Lift = Dado("Lift", "N", "lft", True, False, False, 2, "CELULA")
        self.Drag = Dado("Drag", "N", "drg", True, False, False, 2, "CELULA")
        self.Moment = Dado("Moment", "N", "mmt", True, False, False, 2, "CELULA")
        self.DistCp = Dado("Distance Cp", "m", "dcp", True, False, False, 2, "CELULA")

        self.forcas = []
        for celula in range(self.configurador.NUMERO_DE_CELULAS):
            print(nomeDasCelulas[celula] + ' criada!')
            self.forcas.extend([Dado("Forca - " + nomeDasCelulas[celula], "N", apelidoDasCelulas[celula], True, False, True, 3, "CELULA")])

    def receber_todos_os_dados(self):
        todosOsDados = []

        todosOsDados.extend([
            self.tempo,
            self.mensagemRecebida,
            self.modo,
            self.tamanho
        ])

        #IMU Data
        todosOsDados.extend([
            self.taxaGiroX,
            self.taxaGiroY,
            self.taxaGiroZ,
            self.aceleracaoX,
            self.aceleracaoY,
            self.aceleracaoZ,
            self.pitch,
            self.roll
        ])

        #BARO Data
        todosOsDados.extend([
            self.pressaoTotal,
            self.pressaoEstatica,
            self.pressaoTotalr,
            self.pressaoEstaticar,
            self.temperaturaBar,
            self.densidadeAr,
            self.altitudeRelativa,
            self.altitudePressao
        ])

        #GPS Data
        todosOsDados.extend([
            self.dadoTempoGPS,
            self.latitude,
            self.longitude,
            self.altitude,
            self.direcaoCurso,
            self.velocidade,
            self.velocidadeSubida,
            self.erroX,
            self.erroY,
            self.erroAltitude,
            self.erroVelocidade,
            self.erroVelocidadeSubida,
            self.nivelFixacao,
            self.latitudeRef,
            self.longitudeRef,
            self.posicaoX,
            self.posicaoY,
            self.distanciaAbsoluta
        ])

        #PITOT Data
        for pitot in range(self.configurador.NUMERO_DE_PITOTS):
            todosOsDados.extend([
                self.pressaoDin[pitot],
                self.velCas[pitot]
            ])

        #CELULA Data
        for celula in range(self.configurador.NUMERO_DE_CELULAS):
            todosOsDados.extend([
                self.forcas[celula],
            ])

        todosOsDados.extend([
            self.Lift,
            self.Drag,
            self.Moment,
            self.DistCp
        ])

        return todosOsDados
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
from libs.sonda_aoa import SondaAoA
from libs.arduino import Arduino

from libs.celula import Celula
from libs.balanca import Balanca

from libs.datilografo import Escritor
from libs.telepatia import Transmissor
from configurador import Configurador

class Criador(object):

    def __init__(self, configurador):
        self.configurador = configurador

    def criar_sensores(self):

        if self.configurador.USAR_ARDUINO:
            try:
                self.arduino = Arduino(porta=self.configurador.ARDUINO_PORT)
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
                                                self.configurador.CALFACTS_DOS_PITOTS[i],
                                                self.arduino))
                print('PITOTS ativados!')
            except:
                self.configurador.USAR_PITOTS = False
                print('PITOTS nao ativados!')

        if self.configurador.USAR_SONDAS_AOA:
            try:
                self.sondas_aoa = []
                for i in range(self.configurador.NUMERO_DE_SONDAS_AOA):
                    self.sondas_aoa.append(SondaAoA(self.configurador.NOME_DAS_SONDAS_AOA[i],
                                                    self.configurador.APELIDO_DAS_SONDAS_AOA[i],
                                                    self.configurador.CALFACTS_DAS_SONDAS_AOA[i][0],
                                                    self.configurador.CALFACTS_DAS_SONDAS_AOA[i][1],
                                                    self.configurador.APELIDO_PITOTS_AOA[i][0],
                                                    self.configurador.APELIDO_PITOTS_AOA[i][1],
                                                    self.pitots))
                print('SondasAoA ativadas!')
            except:
                self.configurador.USAR_SONDAS_AOA = False
                print('SondasAoA nao ativadas!')

        if self.configurador.USAR_CELULAS:
            try:
                self.balanca = Balanca()
                self.celulas = []
                for i in range(self.configurador.NUMERO_DE_CELULAS):
                    self.celulas.append(Celula(self.configurador.NOME_DAS_CELULAS[i],
                                                self.configurador.APELIDO_DAS_CELULAS[i],
                                                self.configurador.CALFACTS_DAS_CELULAS[i],
                                                self.arduino))
                print('CELULAS ativadas!')
            except:
                self.configurador.USAR_CELULAS = False
                self.configurador.USAR_BALANCA = False
                print('CELULAS nao ativadas!')

    def criar_escritor(self):
        try:
            self.escritor = Escritor("\t", True, True, self.configurador.NOME_DO_ARQUIVO, ".txt", pasta=self.configurador.PASTA_DESTINO)
            print('Escritor criado!')
        except:
            self.configurador.ATIVAR_GRAVACAO = False
            print('Escritor nao criado!')

    def criar_transmissor(self):
        try:
            self.transmissor = Transmissor(",", True, 57600, 'UTF-8', porta=self.configurador.TRANSMISSOR_PORT)
            self.configurador.ENVIAR_SINAL_DE_VIDA = True
            print('Transmissor criado!')
        except:
            self.configurador.ATIVAR_TRANSMISSAO = False
            self.configurador.ENVIAR_SINAL_DE_VIDA = False
            print('Transmissor nao criado!')

    def criar_dados(self):

        print('Dados gerais criados')

        self.tempo = Dado("Tempo", "seg", "tmp", "GERAL", 4)
        self.mensagemRecebida = Dado("Mensagem", "str", "msg", "GERAL")
        self.modo = Dado("Modo", "int", "mod", "GERAL")
        self.tamanho = Dado("Tamanho do arquivo", "int", "tmn", "GERAL", 3)
        self.angulo_incidencia = Dado("Angulo de incidencia", "deg", "aoi", "GERAL", 3)
        self.angulo_incidencia.setValor(self.configurador.ANGULO_INCIDENCIA)

        print('Dados da IMU criados!')

        self.taxaGiroX = Dado("Taxa de giro em X", "º/s", "gyx", "IMU", 2)
        self.taxaGiroY = Dado("Taxa de giro em Y", "º/s", "gyy", "IMU", 2)
        self.taxaGiroZ = Dado("Taxa de giro em Z", "º/s", "gyz", "IMU", 2)
        self.aceleracaoX = Dado("Aceleração em X", "g", "acx", "IMU", 2)
        self.aceleracaoY = Dado("Aceleração em Y", "g", "acy", "IMU", 2)
        self.aceleracaoZ = Dado("Aceleração em Z", "g", "acz", "IMU", 2)
        self.pitch = Dado("Pitch", "º", "pit", "IMU", 2)
        self.roll = Dado("Roll", "º", "rol", "IMU", 2)

        print('Dados do BARO criados!')

        self.pressaoTotal = Dado("Pressao total", "Pa", "ptt", "BARO", 3)
        self.pressaoEstatica = Dado("Pressao estática", "Pa", "pts", "BARO", 3)
        self.pressaoTotalr = Dado("PTtotal", "Pa", "ptt", "BARO", 3)
        self.pressaoEstaticar = Dado("PTstatic", "Pa", "psr", "BARO", 3)
        self.temperaturaBar = Dado("Temperatura", "ºC", "tem", "BARO", 3)
        self.densidadeAr = Dado("Densidade do ar", "Kg/m³", "den", "BARO", 3)
        self.altitudeRelativa = Dado("Altitude relativa", "m", "alt", "BARO", 3)
        self.altitudePressao = Dado("HP", "ft", "hps", "BARO", 3)

        print('Dados do GPS criados!')

        self.dadoTempoGPS = Dado("Tempo GPS", "-", "tmg", "GPS", 3)
        self.latitude = Dado("Latitude", "º", "lat", "GPS", 6)
        self.longitude = Dado("Longitude", "º", "lng", "GPS", 6)
        self.altitude = Dado("ZGPS", "m", "atg", "GPS", 2)
        self.direcaoCurso = Dado("Direção de curso", "º", "cog", "GPS", 1)
        self.velocidade = Dado("Velocidade GPS", "m/s", "vel", "GPS", 2)
        self.velocidadeSubida = Dado("Velocidade de subida", "m/s","ves", "GPS", 2)
        self.erroX = Dado("Erro em X", "m", "erx", "GPS", 1)
        self.erroY = Dado("Erro em Y", "m", "ery", "GPS", 1)
        self.erroAltitude = Dado("Erro da altitude", "m", "era", "GPS", 1)
        self.erroVelocidade = Dado("Erro de velocidade", "nós", "ers", "GPS", 1)
        self.erroVelocidadeSubida = Dado("Erro da velocidade de subida", "m/s", "ves", "GPS", 1)
        self.nivelFixacao = Dado("Nivel de fixação GPS", "-", "nfx", "GPS", 1)
        self.latitudeRef = Dado("Latitude de referência", "-", "ltr", "GPS", 6)
        self.longitudeRef = Dado("Longitude de referência", "-", "lgr", "GPS", 6)
        self.posicaoX = Dado("XGPS", "m", "gpx", "GPS", 2)
        self.posicaoY = Dado("YGPS", "m", "gpy", "GPS", 2)
        self.distanciaAbsoluta = Dado("Distancia absoluta", "m", "dtr", "GPS", 2)

        print('Dados dos PITOTS criados!')

        nomeDosPitots = self.configurador.NOME_DOS_PITOTS
        apelidoDosPitots = self.configurador.APELIDO_DOS_PITOTS

        self.rawPitotData = []
        self.pressaoDinRef = []
        self.velCasRef = []

        for pitot in range(self.configurador.NUMERO_DE_PITOTS):
            print(nomeDosPitots[pitot] + ' criado!')
            self.rawPitotData.extend([Dado("Raw Pitot Data - " + nomeDosPitots[pitot], "V", apelidoDosPitots[pitot] + '_raw', "PITOT", 3)])
            self.pressaoDinRef.extend([Dado("Pressao Dinamica Ref.- " + nomeDosPitots[pitot], "Pa", 'pd_' + apelidoDosPitots[pitot] + '_ref', "PITOT", 3)])
            self.velCasRef.extend([Dado("VCAS Ref. - " + nomeDosPitots[pitot], "m/s", "vcs_" + apelidoDosPitots[pitot] + '_ref', "PITOT", 4)])

        print('Dados das SONDAS_AOA criados!')

        nomeDasSondasAoA = self.configurador.NOME_DAS_SONDAS_AOA
        apelidoDasSondasAoA = self.configurador.APELIDO_DAS_SONDAS_AOA

        self.aoa_dif_press = []
        self.aoa_dyn_press = []
        self.aoa = []

        for sonda_aoa in range(self.configurador.NUMERO_DE_SONDAS_AOA):
            print(nomeDasSondasAoA[sonda_aoa] + ' criada!')
            self.aoa_dif_press.extend([Dado("AoA Differential Pressure - " + nomeDasSondasAoA[sonda_aoa], "Pa", apelidoDasSondasAoA[sonda_aoa] + '_dfp', "SONDA_AOA", 3)])
            self.aoa_dyn_press.extend([Dado("AoA Dynamic Pressure - " + nomeDasSondasAoA[sonda_aoa], "Pa", apelidoDasSondasAoA[sonda_aoa] + '_dnp', "SONDA_AOA", 3)])
            self.aoa.extend([Dado("AoA - " + nomeDasSondasAoA[sonda_aoa], "deg", apelidoDasSondasAoA[sonda_aoa], "SONDA_AOA", 3)])

        print('Dados das CELULAS criados!')

        nomeDasCelulas = self.configurador.NOME_DAS_CELULAS
        apelidoDasCelulas = self.configurador.APELIDO_DAS_CELULAS

        self.Lift = Dado("Lift", "N", "lft", "CELULA", 3)
        self.Drag = Dado("Drag", "N", "drg", "CELULA", 3)
        self.Moment = Dado("Moment", "N", "mmt", "CELULA", 3)
        self.DistCp = Dado("Distance Cp", "m", "dcp", "CELULA", 3)

        self.rawCellData = []
        self.forcas = []
        for celula in range(self.configurador.NUMERO_DE_CELULAS):
            print(nomeDasCelulas[celula] + ' criada!')
            self.rawCellData.extend([Dado("Raw Cell Data - " + nomeDasCelulas[celula], "adm", apelidoDasCelulas[celula] + '_raw', "CELULA", 3)])
            self.forcas.extend([Dado("Forca - " + nomeDasCelulas[celula], "N", apelidoDasCelulas[celula], "CELULA", 3)])

    def receber_todos_os_dados(self):
        todosOsDados = []

        todosOsDados.extend([
            self.tempo,
            self.mensagemRecebida,
            self.modo,
            self.tamanho,
            self.angulo_incidencia
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
                self.rawPitotData[pitot],
                self.pressaoDinRef[pitot],
                self.velCasRef[pitot]
            ])

        #SONDA_AOA Data
        for sonda_aoa in range(self.configurador.NUMERO_DE_SONDAS_AOA):
            todosOsDados.extend([
                self.aoa_dif_press[sonda_aoa],
                self.aoa_dyn_press[sonda_aoa],
                self.aoa[sonda_aoa]
            ])

        #CELULA Data
        for celula in range(self.configurador.NUMERO_DE_CELULAS):
            todosOsDados.extend([
                self.rawCellData[celula],
                self.forcas[celula]
            ])

        todosOsDados.extend([
            self.Lift,
            self.Drag,
            self.Moment,
            self.DistCp
        ])

        return todosOsDados
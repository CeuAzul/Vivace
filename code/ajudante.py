#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
from datetime import datetime

from libs.datilografo import Escritor
from libs.telepatia import Transmissor
from libs.dado import Dado

from libs.mpu import MPU
from libs.barometro import Barometro
from libs.gps import GPS
from libs.pitot import Pitot
from libs.arduino import Arduino

from libs.celula import Celula
from libs.balanca import Balanca

# from modos_de_transmissao import SeletorDeModos

class Ajudante(object):

    def __init__(self, configurador, criador):
        self.configurador = configurador
        self.criador = criador
        # self.seletorDeModos = SeletorDeModos()
        self.telecomandoExecutado = False
        self.threadsRodando = True
        self.inicioDoDia = datetime(datetime.now().year,
                                    datetime.now().month,
                                    datetime.now().day)
        self.tempoAtual = (datetime.now() - self.inicioDoDia).total_seconds()
        self.NaN = float('nan')
        self.tempoGPS = self.NaN
        self.utc = self.NaN
        self.sensores = ["IMU", "BARO", "GPS", "PITOT", "CELULA"]

    def ativar_sensores(self):
        if self.configurador.USAR_IMU == True:
            print('IMU ativada!')
            self.mpu = MPU(True, True, True, True, True, True, True, True)
        if self.configurador.USAR_BARO == True:
            print('BARO ativada!')
            self.barometro = Barometro(True, True)
        if self.configurador.USAR_GPS == True:
            print('GPS ativada!')
            self.gps = GPS()
        if self.configurador.USAR_PITOTS == True:
            print('PITOTS ativados!')
            self.pitots = []
            for i in range(self.configurador.NUMERO_DE_PITOTS):
                self.pitots.append(Pitot(self.configurador.NOME_DOS_PITOTS[i],
                                            self.configurador.APELIDO_DOS_PITOTS[i]))
        if self.configurador.USAR_ARDUINO == True:
            print('ARDUINO ativado!')
            self.arduino = Arduino()

            if self.configurador.USAR_CELULAS == True:
                print('CELULAS ativadas!')
                self.balanca = Balanca()
                self.celulas = []
                for i in range(self.configurador.NUMERO_DE_CELULAS):
                    self.celulas.append(Celula(self.configurador.NOME_DAS_CELULAS[i],
                                                self.configurador.APELIDO_DAS_CELULAS[i]))

    def receber_dados_usados(self):

        pacoteDeDados = []
        todosOsDados = self.criador.receber_todos_os_dados()

        pacoteDeDados.extend([
            self.criador.tempo,
            self.criador.mensagemRecebida,
            self.criador.modo,
            self.criador.tamanho
        ])

        for dado in todosOsDados:
            if dado.sensor == 'IMU':
                if self.configurador.USAR_IMU:
                    pacoteDeDados.extend([dado])
            if dado.sensor == 'BARO':
                if self.configurador.USAR_BARO:
                    pacoteDeDados.extend([dado])
            if dado.sensor == 'GPS':
                if self.configurador.USAR_GPS:
                    pacoteDeDados.extend([dado])
            if dado.sensor == 'PITOT':
                if self.configurador.USAR_PITOTS:
                    pacoteDeDados.extend([dado])
            if dado.sensor == 'CELULA':
                if self.configurador.USAR_CELULAS:
                    pacoteDeDados.extend([dado])

        return pacoteDeDados

    def ativar_transmissao(self, sensor):

        dados = self.receber_pacote_de_dados()

        for dado in todosOsDados:
            if dado.sensor == sensor:
                print(dado.nome + ' sendo transmitido')
                dado.setTransmissao(True)

    def criar_escritor_transmissor(self):
        print('Escritor e Transmissor criados!')
        self.escritor = Escritor("\t", True, True, self.configurador.NOME_DO_ARQUIVO + "- ", ".txt", pasta=self.configurador.PASTA_DESTINO)
        self.transmissor = Transmissor(",", True, 57600, 'UTF-8')

    def criar_novo_arquivo(self):
        print('Novo arquivo sendo criado!')
        self.escritor
        modoAtual = self.modo.getValor()
        self.trocarModoDeTransmissao(0)
        del self.escritor
        self.escritor = Escritor("\t", True, True, self.configurador.NOME_DO_ARQUIVO + "- ", ".txt", pasta=self.configurador.PASTA_DESTINO)
        self.escritor.setDados(self.receber_dados_usados())
        self.trocarModoDeTransmissao(modoAtual)

    def trocarModoDeTransmissao(self, modo):
        self.criador.modo.setValor(modo)
        print('Trocando para modo ' + str(modo) + ' de transmissao!')
        # seletorDeModos.set

    def liga_threads(self):
        print('Ligando as threads!')
        self.threadsRodando = True

    def desliga_threads(self):
        print('Desligando as threads!')
        self.threadsRodando = False

    def transmitirDados(self, delay):
        while self.threadsRodando:
            print('Transmitindo dados!')
            self.transmissor.setDados(self.receber_dados_usados)
            self.transmissor.transmiteLinha()
            time.sleep(delay)

    def gravarDados(self, delay):
        while self.threadsRodando == True:
            print('Gravando dados!')
            self.tempoAtual = (datetime.now() - self.inicioDoDia).total_seconds()
            self.criador.tempo.setValor(self.tempoAtual)
            if self.criador.modo.getValor() == 4:
                self.escritor.setDados(self.receber_dados_usados())
                self.escritor.escreveLinhaDado()
            time.sleep(delay)

    def lerTelecomando(self, delay):
        while self.threadsRodando:
            print('Lendo telecomando!')

            self.criador.tamanho.setValor(self.escritor.verificaTamanhoArquivo())
            comandoRecebido = self.transmissor.leLinha()
            self.criador.mensagemRecebida.setValor(comandoRecebido)
            if comandoRecebido == "@t#c%$0#1$":
                if self.telecomandoExecutado == False:
                    self.telecomandoExecutado = True
                    self.trocarModoDeTransmissao(4)
                else:
                    self.telecomandoExecutado = False
            time.sleep(delay)


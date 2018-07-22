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

class Ajudante(object):

    def __init__(self, configurador, criador, seletor):
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
        self.sensores = ["IMU", "BARO", "GPS", "PITOT", "SONDA_AOA", "CELULA"]
        self.seletor = seletor

    def receber_dados_usados(self):

        pacoteDeDados = []
        todosOsDados = self.criador.receber_todos_os_dados()

        pacoteDeDados.extend([
            self.criador.tempo,
            self.criador.mensagemRecebida,
            self.criador.modo,
            self.criador.tamanho,
            self.criador.angulo_incidencia,
            self.criador.velocidadeCarro
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
            if dado.sensor == 'SONDA_AOA':
                if self.configurador.USAR_SONDAS_AOA:
                    pacoteDeDados.extend([dado])
            if dado.sensor == 'CELULA':
                if self.configurador.USAR_CELULAS:
                    pacoteDeDados.extend([dado])

        return pacoteDeDados

    def criar_novo_arquivo(self):
        print('Novo arquivo sendo criado!')
        self.criador.escritor
        modoAtual = self.modo.getValor()
        del self.criador.escritor
        self.criador.escritor = Escritor("\t", True, True, self.configurador.NOME_DO_ARQUIVO, ".txt", pasta=self.configurador.PASTA_DESTINO)
        self.criador.escritor.setDados(self.receber_dados_usados())

    def ativar_transmissao(self, sensor):

        dadosUsados = self.receber_dados_usados()

        for dado in dadosUsados:
            if dado.sensor == sensor:
                print('Transmissao de ' + dado.nome + ' ativada!')
                dado.setTransmissao(True)

    def liga_threads(self):
        print('Ligando as threads!')
        self.threadsRodando = True

    def desliga_threads(self):
        print('Desligando as threads!')
        self.threadsRodando = False

    def transmitirDados(self, delay):
        while self.threadsRodando:
            self.criador.transmissor.setDados(self.receber_dados_usados())
            self.criador.transmissor.transmiteLinha()
            time.sleep(delay)

    def gravarDados(self, delay):
        while self.threadsRodando == True:
            self.tempoAtual = (datetime.now() - self.inicioDoDia).total_seconds()
            self.criador.tempo.setValor(self.tempoAtual)
            if self.criador.modo.getValor() == 4:
                self.criador.escritor.setDados(self.receber_dados_usados())
                self.criador.escritor.escreveLinhaDado()
            time.sleep(delay)

    def lerTelecomando(self, delay):
        while self.threadsRodando:

            self.criador.tamanho.setValor(self.criador.escritor.verificaTamanhoArquivo())
            comandoRecebido = self.criador.transmissor.leLinha()
            self.criador.mensagemRecebida.setValor(comandoRecebido)


            if comandoRecebido.startswith('!') and comandoRecebido.endswith('@'):
                if not self.telecomandoExecutado:
                    self.telecomandoExecutado = True

                    if comandoRecebido == "@t#c%$0#1$":
                        print('mudando modo para 4')
                        self.seletor.setModo(4)
                    if comandoRecebido == "!tc@":
                        print('tarando celulas')
                        self.criador.arduino.sendCommand('tc')
                    if comandoRecebido == "!pp@":
                        self.criador.arduino.sendCommand('pp')
                    if comandoRecebido == "!pc@":
                        self.criador.arduino.sendCommand('pc')
                    if comandoRecebido == "!so@":
                        self.criador.arduino.sendCommand('so')
                    if comandoRecebido == "!zp@":
                        for i in range(self.configurador.NUMERO_DE_PITOTS):
                            self.criador.pitots[i].setRefPitot()

                else:
                    self.telecomandoExecutado = False
            time.sleep(delay)


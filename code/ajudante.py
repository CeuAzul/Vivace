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
        self.seletor = seletor

        self.threadsRodando = True
        self.transmitindo = False
        self.gravando = False

        self.configuracoes_recebidas = False
        self.telecomandoExecutado = False

        self.NaN = float('nan')
        self.tempoGPS = self.NaN
        self.utc = self.NaN
        self.sensores = ["IMU", "BARO", "GPS", "PITOT", "SONDA_AOA", "CELULA"]

    def receber_dados_usados(self):

        pacoteDeDados = []
        todosOsDados = self.criador.receber_todos_os_dados()

        pacoteDeDados.extend([
            self.criador.tempo,
            self.criador.mensagemRecebida,
            self.criador.modo,
            self.criador.tamanho,
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

    def liga_transmissao(self):
        print('Ligando transmissao!')
        self.transmitindo = True

    def desliga_transmissao(self):
        print('Desligando transmissao!')
        self.transmitindo = False

    def liga_gravacao(self):
        print('Ligando gravaçao!')
        self.gravando = True

    def desliga_gravacao(self):
        print('Desligando gravaçao!')
        self.gravando = False

    def transmitirDados(self, delay):
        while self.threadsRodando:
            if self.transmitindo:
                self.criador.transmissor.setDados(self.receber_dados_usados())
                self.criador.transmissor.transmiteLinha()
            time.sleep(delay)

    def gravarDados(self, delay):
        while self.threadsRodando:
            if self.gravando:
                self.criador.escritor.setDados(self.receber_dados_usados())
                self.criador.escritor.escreveLinhaDado()
            time.sleep(delay)

    def lerTelecomando(self, delay):
        while self.threadsRodando:
            comandoRecebido = self.criador.transmissor.leLinha()
            self.criador.mensagemRecebida.setValor(comandoRecebido)

            if comandoRecebido.startswith('!') and comandoRecebido.endswith('@'):
                comandoRecebido = comandoRecebido.replace("!", "")
                comandoRecebido = comandoRecebido.replace("@", "")

                if comandoRecebido == "tc":
                    print('Tarando Celulas!')
                    try:
                        self.criador.arduino.sendCommand('tc')
                    except:
                        pass
                if comandoRecebido == "zp":
                    print('Tarando Pitots!')
                    for i in range(self.configurador.NUMERO_DE_PITOTS):
                        try:
                            self.criador.pitots[i].setRefPitot()
                        except:
                            pass
                if (comandoRecebido == "@t#c%$0#1$"):
                    print('Iniciando gravação + recepção normal')
                    self.seletor.setModo(4)
                if (comandoRecebido == "@%&*v##&(@"):
                    print('Transmitindo apenas Vcas, hp, RPM e altitude gps')
                    self.seletor.setModo(2)
                if (comandoRecebido == "&*$$%#!@&_"):
                    print('Ativando somente a transmissao')
                    self.seletor.setModo(3)
                if (comandoRecebido == "*)(#$%@!&*"):
                    print('Pausando gravaçao')
                    self.seletor.setModo(0)
                if (comandoRecebido == "AqT%$BNy*("):
                    print('Criando novo arquivo')
                    self.criar_novo_arquivo()
                if (comandoRecebido == "spd"):
                    print('Passando dados para o pendrive')
                    escritor.passaProPendrive()
                if (comandoRecebido == "rp"):
                    print('Reiniciando a plataforma')
                    os.system('sudo reboot')
                if (comandoRecebido == "sp"):
                    print('Desligando plataforma')
                    os.system('sudo shutdown now')
                if (comandoRecebido == 'sc'):
                    print('Configuraçoes recebidas')
                    self.configuracoes_recebidas = True
                if (comandoRecebido == 'dg'):
                    print('Gravaçao desligada')
                    self.desliga_gravacao()
                if (comandoRecebido == 'lg'):
                    print('Gravaçao ligada')
                    self.liga_gravacao()
                if (comandoRecebido == 'dt'):
                    print('Transmissao desligada')
                    self.desliga_transmissao()
                if (comandoRecebido == 'lt'):
                    print('Transmissao ligada')
                    self.liga_transmissao()
                if (comandoRecebido.startswith('config')):
                    self.configurar_configurador(comandoRecebido)

                time.sleep(delay)

    def configurar_configurador(self, comandoRecebido):

        comandoRecebido = comandoRecebido.replace('config:', '')
        configs = comandoRecebido.split(";")
        for config in configs:
            try:
                chave, valor = config.split("=")

                if chave == 'NOME_DA_AERONAVE':
                    self.configurador.NOME_DA_AERONAVE = valor
                if chave == 'LOCAL_DE_VOO':
                    self.configurador.LOCAL_DE_VOO = valor
                if chave == 'TEMPERATURA':
                    self.configurador.TEMPERATURA = valor
                if chave == 'ANGULO_INCIDENCIA_ASA':
                    self.configurador.ANGULO_INCIDENCIA_ASA = valor
                if chave == 'ANGULO_INCIDENCIA_PROFUNDOR':
                    self.configurador.ANGULO_INCIDENCIA_PROFUNDOR = valor
                if chave == 'INFOS_EXTRAS':
                    self.configurador.INFOS_EXTRAS = valor

                print('Configuraçao: ' + chave + ' = ' + valor)
            except:
                pass
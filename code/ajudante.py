#!/usr/bin/python
# -*- coding: utf-8 -*-

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

        self.NaN = float('nan')
        self.tempoGPS = self.NaN
        self.utc = self.NaN

    def criar_novo_arquivo(self):
        print('Criando novo arquivo')
        self.criador.escritor
        modoAtual = self.modo.getValor()
        del self.criador.escritor
        self.criador.escritor = Escritor("\t", True, True, self.configurador.NOME_DO_ARQUIVO, ".txt", pasta=self.configurador.PASTA_DESTINO)
        self.criador.escritor.dados = self.criador.receber_todos_os_dados()

    def ativar_transmissao(self, sensor):
        dadosUsados = self.criador.receber_todos_os_dados()
        for dado in dadosUsados:
            if dado.sensor == sensor:
                print('Transmissao de ' + dado.nome + ' ativada')
                dado.transmiteDado = True

    def setar_transmissao_seletiva(self, comandoRecebido):

        config = comandoRecebido.replace('sts:', '')
        try:
            apelido, estado = config.split("=")
        except:
            pass

        dadosUsados = self.criador.receber_todos_os_dados()

        for dado in dadosUsados:
            if dado.apelido == apelido:
                if estado == 'True':
                    dado.transmiteDado = True
                    print('Transmissao de ' + dado.nome + ' ativada')
                elif estado == 'False':
                    dado.transmiteDado = False
                    print('Transmissao de ' + dado.nome + ' desativada')

    def desativar_transmissao_generalizada(self):
        dadosUsados = self.criador.receber_todos_os_dados()
        for dado in dadosUsados:
            dado.transmiteDado = False

    def liga_threads(self):
        print('Ligando as threads')
        self.threadsRodando = True

    def desliga_threads(self):
        print('Desligando as threads')
        self.threadsRodando = False

    def liga_transmissao(self):
        print('Ligando transmissao')
        self.transmitindo = True

    def desliga_transmissao(self):
        print('Desligando transmissao')
        self.transmitindo = False

    def liga_gravacao(self):
        print('Ligando gravaçao')
        self.gravando = True

    def desliga_gravacao(self):
        print('Desligando gravaçao')
        self.gravando = False

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
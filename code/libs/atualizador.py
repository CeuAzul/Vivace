#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
from datetime import datetime
import math
import os
import sys

class Atualizador(object):

    def __init__(self, configurador, criador, ajudante):
        self.configurador = configurador
        self.criador = criador
        self.ajudante = ajudante

        self.initialTime = datetime.now()
        self.atualizandoReferenciaDoBarometro = False


    def atualizarIMU(self, delay):
        """Esta função é utilizada como o processo periódico que
        irá adquirir os dados da IMU.

        :param delay: Valor com o tempo entre cada atualização.
        """
        while self.ajudante.threadsRodando:
            self.criador.imu.atualiza()
            self.criador.taxaGiroX.valor = self.criador.imu.gyx
            self.criador.taxaGiroY.valor = self.criador.imu.gyy
            self.criador.taxaGiroZ.valor = self.criador.imu.gyz
            self.criador.aceleracaoX.valor = self.criador.imu.acx
            self.criador.aceleracaoY.valor = self.criador.imu.acy
            self.criador.aceleracaoZ.valor = self.criador.imu.acz
            time.sleep(delay)


    def atualizarBarometro(self, delay):
        """Esta função é utilizada como o processo periódico que
        irá adquirir dados do barômetro.

        :param delay: Valor com o tempo entre cada atualização.
        """
        while self.ajudante.threadsRodando:
            if self.atualizandoReferenciaDoBarometro == True:
                self.criador.barometro.atualizaReferencia()
                atualizaRefBar = False
            self.criador.barometro.atualiza()
            self.criador.pressaoEstatica.valor = self.criador.barometro.pressao
            self.criador.pressaoEstaticaReferenciada.valor = self.criador.barometro.pressaoReferenciada
            self.criador.temperaturaBar.valor = self.criador.barometro.temperatura
            self.criador.densidadeAr.valor = self.criador.barometro.densidadeAr
            self.criador.altitudeRelativa.valor = self.criador.barometro.altitudeRelativa
            self.criador.altitudePressao.valor = self.criador.barometro.altitudePressao
            time.sleep(delay)

    def atualizarGps(self, delay):
        """Esta função é utilizada como o processo periódico que
        irá adquirir dados do gps.

        :param delay: Valor com o tempo entre cada atualização.
        """
        while self.ajudante.threadsRodando:
            self.criador.gps.atualiza()
            self.criador.latitude.valor = self.criador.gps.latitude
            self.criador.longitude.valor = self.criador.gps.longitude
            self.criador.altitude.valor = self.criador.gps.altitude
            self.criador.direcaoCurso.valor = self.criador.gps.direcaoCurso
            self.criador.velocidade.valor = self.criador.gps.velocidade
            self.criador.velocidadeSubida.valor = self.criador.gps.velocidadeSubida
            self.criador.erroX.valor = self.criador.gps.erroX
            self.criador.erroY.valor = self.criador.gps.erroY
            self.criador.erroAltitude.valor = self.criador.gps.erroAltitude
            self.criador.erroVelocidade.valor = self.criador.gps.erroVelocidade
            self.criador.erroVelocidadeSubida.valor = self.criador.gps.erroVelocidadeSubida
            self.criador.nivelFixacao.valor = self.criador.gps.nivelFixacao
            self.criador.latitudeRef.valor = self.criador.gps.latitudeRef
            self.criador.longitudeRef.valor = self.criador.gps.longitudeRef
            self.criador.posicaoX.valor = self.criador.gps.posicaoX
            self.criador.posicaoY.valor = self.criador.gps.posicaoY
            self.criador.distanciaAbsoluta.valor = self.criador.gps.distanciaAbsoluta
            self.criador.tempoGps = self.criador.gps.utc
            self.criador.dadoTempoGPS.valor = self.criador.gps.tempo

            agora = datetime.now()
            inicioDia = datetime(agora.year, agora.month, agora.day)

            if (self.criador.gps.verificaAtualizacaoHorario()) and (self.ajudante.modo.valor == 0):
                self.ajudante.trocarModoDeTransmissao(1)

            time.sleep(delay)
            self.ajudante.gps.finaliza()


    def atualizarPitot(self, delay):
        """Esta função é utilizada como o processo periódico que
        irá adquirir dados do pitot.

        :param delay: Valor com o tempo entre cada atualização.
        """
        while self.ajudante.threadsRodando:
            for i in range(self.configurador.NUMERO_DE_PITOTS):
                self.criador.pitots[i].atualiza()
                self.criador.rawPitotData[i].valor = self.criador.pitots[i].rawPitotData
                self.criador.pressaoDinRef[i].valor = self.criador.pitots[i].pressaoDinamicaRef
                self.criador.velRef[i].valor = self.criador.pitots[i].velocidadeRef
            time.sleep(delay)

    def atualizarSondasAoA(self, delay):
        """Esta função é utilizada como o processo periódico que
        irá adquirir dados das Sondas AoA.

        :param delay: Valor com o tempo entre cada atualização.
        """
        while self.ajudante.threadsRodando:
            for i in range(self.configurador.NUMERO_DE_SONDAS_AOA):
                self.criador.sondas_aoa[i].atualiza(samples=10)
                self.criador.aoa_dif_press[i].valor = self.criador.sondas_aoa[i].difPressure
                self.criador.aoa_dyn_press[i].valor = self.criador.sondas_aoa[i].dynPressure
                self.criador.aoa[i].valor = self.criador.sondas_aoa[i].aoa
            time.sleep(delay)


    def atualizarArduino(self, delay):
        """Esta função é utilizada como o processo periódico que
        irá adquirir dados do Arduino.

        :param delay: Valor com o tempo entre cada atualização.
        """
        while self.ajudante.threadsRodando:
            self.criador.arduino.updateData()

            time.sleep(delay)

    def atualizarCelulas(self, delay):
        """Esta função é utilizada como o processo periódico que
        irá adquirir atualizar os dados de força da balança.

        :param delay: Valor com o tempo entre cada atualização.
        """
        while self.ajudante.threadsRodando:
            for i in range(self.configurador.NUMERO_DE_CELULAS):
                self.criador.celulas[i].atualiza()
                self.criador.rawCellData[i].valor = self.criador.celulas[i].rawCellData
                self.criador.forcas[i].valor = self.criador.celulas[i].force

            time.sleep(delay)

    def atualizarBalanca(self, delay):
        """Esta função é utilizada como o processo periódico que
        irá adquirir atualizar os dados de força da balança.

        :param delay: Valor com o tempo entre cada atualização.
        """
        while self.ajudante.threadsRodando:
            self.criador.balanca.updateForces(self.criador.forcas[0].valor,
                                                self.criador.forcas[1].valor,
                                                self.criador.forcas[2].valor,
                                                self.criador.forcas[3].valor,
                                                self.criador.forcas[4].valor)

            self.criador.Lift.valor = self.criador.balanca.Lift
            self.criador.Drag.valor = self.criador.balanca.Drag
            self.criador.Moment.valor = self.criador.balanca.Moment
            self.criador.DistCp.valor = self.criador.balanca.Dist_Cp_front

            time.sleep(delay)

    def transmitirDados(self, delay):
        while self.ajudante.threadsRodando:
            if self.ajudante.transmitindo:
                self.criador.transmissor.dados = self.criador.receber_todos_os_dados()
                self.criador.transmissor.transmiteLinha()
            time.sleep(delay)

    def gravarDados(self, delay):
        while self.ajudante.threadsRodando:
            if self.ajudante.gravando:
                self.criador.escritor.dados = self.criador.receber_todos_os_dados()
                self.criador.escritor.escreveLinhaDado()
            time.sleep(delay)

    def enviarSinalDeVida(self, delay):
        index = 0
        while self.ajudante.threadsRodando:
            index += 1
            if index >= 360:
                index = 0
            seno = math.sin(math.radians(index))
            self.criador.transmissor.transmiteDadoProtocolado("htb", 1)
            self.criador.transmissor.transmiteDadoProtocolado("tmt", int(self.ajudante.transmitindo))
            self.criador.transmissor.transmiteDadoProtocolado("gvd", int(self.ajudante.gravando))
            self.criador.transmissor.transmiteDadoProtocolado("cfg", int(self.ajudante.configuracoes_recebidas))
            self.criador.transmissor.transmiteDadoProtocolado("idx", index)
            self.criador.transmissor.transmiteDadoProtocolado("sin", seno)
            print(seno)
            time.sleep(delay)

    def atualizarGeral(self, delay):
        while self.ajudante.threadsRodando:
            self.criador.tempo.valor = (datetime.now() - self.initialTime).total_seconds()
            self.criador.tamanho.valor = self.criador.escritor.verificaTamanhoArquivo()
            time.sleep(delay)

    def lerTelecomando(self, delay):
        while self.ajudante.threadsRodando:
            comandoRecebido = self.criador.transmissor.leLinha()
            self.criador.mensagemRecebida.valor = comandoRecebido

            if comandoRecebido.startswith('!') and comandoRecebido.endswith('@'):
                comandoRecebido = comandoRecebido.replace("!", "")
                comandoRecebido = comandoRecebido.replace("@", "")

                if comandoRecebido == "tc":
                    print('Tarando Celulas')
                    try:
                        self.criador.arduino.sendCommand('tc')
                    except:
                        pass
                if comandoRecebido == "zp":
                    print('Tarando Pitots')
                    for i in range(self.configurador.NUMERO_DE_PITOTS):
                        try:
                            self.criador.pitots[i].setRefPitot()
                        except:
                            pass

                if (comandoRecebido == "AqT%$BNy*("):
                    self.ajudante.criar_novo_arquivo()
                if (comandoRecebido == "spd"):
                    print('Passando dados para o pendrive')
                    self.criador.escritor.passaProPendrive()
                if (comandoRecebido == "rp"):
                    print('Reiniciando a plataforma')
                    os.system('sudo reboot')
                if (comandoRecebido == "sp"):
                    print('Desligando plataforma')
                    os.system('sudo shutdown now')
                if (comandoRecebido == 'sc'):
                    print('Recebendo configuraçoes')
                    self.ajudante.configuracoes_recebidas = True
                if (comandoRecebido == 'dg'):
                    self.ajudante.desliga_gravacao()
                if (comandoRecebido == 'lg'):
                    self.ajudante.liga_gravacao()
                if (comandoRecebido == 'dt'):
                    self.ajudante.desliga_transmissao()
                if (comandoRecebido == 'lt'):
                    self.ajudante.liga_transmissao()
                if (comandoRecebido == 'dtg'):
                    self.ajudante.desativar_transmissao_generalizada()
                if (comandoRecebido.startswith('sts')):
                    self.ajudante.setar_transmissao_seletiva(comandoRecebido)
                if (comandoRecebido == 'ft'):
                    print('Finalizando teste')
                    os.execv(sys.executable, ['python3'] + sys.argv)
                if (comandoRecebido.startswith('config')):
                    self.ajudante.configurar_configurador(comandoRecebido)

            time.sleep(delay)
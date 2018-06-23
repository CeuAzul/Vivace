#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
from datetime import datetime

class Atualizador(object):

    def __init__(self, configurador, criador, ajudante):
        self.configurador = configurador
        self.criador = criador
        self.ajudante = ajudante

        self.atualizandoReferenciaDoBarometro = False


    def atualizarIMU(self, delay):
        """Esta função é utilizada como o processo periódico que
        irá adquirir os dados da IMU.

        :param delay: Valor com o tempo entre cada atualização.
        """
        while self.ajudante.threadsRodando:
            print('Puxando dados da IMU!')

            self.ajudante.mpu.atualiza()
            self.criador.taxaGiroX.setValor(self.ajudante.mpu.getGyx())
            self.criador.taxaGiroY.setValor(self.ajudante.mpu.getGyy())
            self.criador.taxaGiroZ.setValor(self.ajudante.mpu.getGyz())
            self.criador.aceleracaoX.setValor(self.ajudante.mpu.getAcx())
            self.criador.aceleracaoY.setValor(self.ajudante.mpu.getAcy())
            self.criador.aceleracaoZ.setValor(self.ajudante.mpu.getAcz())
            self.criador.pitch.setValor(self.ajudante.mpu.getPitch())
            self.criador.roll.setValor(self.ajudante.mpu.getRoll())
            time.sleep(delay)


    def atualizarBarometro(self, delay):
        """Esta função é utilizada como o processo periódico que
        irá adquirir dados do barômetro.

        :param delay: Valor com o tempo entre cada atualização.
        """
        while self.ajudante.threadsRodando:
            print('Puxando dados do BARO!')

            if self.atualizandoReferenciaDoBarometro == True:
                self.ajudante.barometro.atualizaReferencia()
                atualizaRefBar = False
            self.ajudante.barometro.atualiza()
            self.criador.pressaoEstatica.setValor(self.ajudante.barometro.getPressao("PA"))
            self.criador.pressaoEstaticar.setValor(self.ajudante.barometro.getPressao("PA"))
            self.criador.pressaoTotal.setValor(self.ajudante.barometro.getPressao("PA") + self.ajudante.pitot.getPressaoDinamica("PA"))
            self.criador.pressaoTotalr.setValor(self.ajudante.barometro.getPressao("PA") + self.ajudante.pitot.getPressaoDinamica("PA"))
            self.criador.temperaturaBar.setValor(self.ajudante.barometro.getTemperatura())
            self.criador.densidadeAr.setValor(self.ajudante.barometro.getDensidadeAr())
            self.criador.altitudeRelativa.setValor(self.ajudante.barometro.getAltitudeRelativa("m"))
            self.criador.altitudePressao.setValor(self.ajudante.barometro.getAltitudePressao("ft"))
            time.sleep(delay)

    def atualizarGps(self, delay):
        """Esta função é utilizada como o processo periódico que
        irá adquirir dados do gps.

        :param delay: Valor com o tempo entre cada atualização.
        """
        while self.ajudante.threadsRodando:
            print('Puxando dados do GPS!')

            self.ajudante.gps.atualiza()
            self.criador.latitude.setValor(self.ajudante.gps.getLatitude())
            self.criador.longitude.setValor(self.ajudante.gps.getLongitude())
            self.criador.altitude.setValor(self.ajudante.gps.getAltitude())
            self.criador.direcaoCurso.setValor(self.ajudante.gps.getDirecaoCurso())
            self.criador.velocidade.setValor(self.ajudante.gps.getVelocidade())
            self.criador.velocidadeSubida.setValor(self.ajudante.gps.getVelSubida())
            self.criador.erroX.setValor(self.ajudante.gps.getErroX())
            self.criador.erroY.setValor(self.ajudante.gps.getErroY())
            self.criador.erroAltitude.setValor(self.ajudante.gps.getErroAltitude())
            self.criador.erroVelocidade.setValor(self.ajudante.gps.getErroVelocidade())
            self.criador.erroVelocidadeSubida.setValor(self.ajudante.gps.getErroVelSubida())
            self.criador.nivelFixacao.setValor(self.ajudante.gps.getNivelFixacao())
            self.criador.latitudeRef.setValor(self.ajudante.gps.getLatitudeRef())
            self.criador.longitudeRef.setValor(self.ajudante.gps.getLongitudeRef())
            self.criador.posicaoX.setValor(self.ajudante.gps.getPosicaoX())
            self.criador.posicaoY.setValor(self.ajudante.gps.getPosicaoY())
            self.criador.distanciaAbsoluta.setValor(self.ajudante.gps.getDistanciaAbsoluta())
            self.criador.tempoGps = self.gps.ajudante.getTempo()
            self.criador.dadoTempoGPS.setValor(self.ajudante.tempoGps)

            agora = datetime.now()
            inicioDia = datetime(agora.year, agora.month, agora.day)

            if (self.ajudante.gps.verificaAtualizacaoHorario()) and (self.ajudante.modo.getValor() == 0):
                self.ajudante.trocarModoDeTransmissao(1)

            time.sleep(delay)
            self.ajudante.gps.finaliza()


    def atualizarPitot(self, delay):
        """Esta função é utilizada como o processo periódico que
        irá adquirir dados do pitot.

        :param delay: Valor com o tempo entre cada atualização.
        """
        while self.ajudante.threadsRodando:
            print('Puxando dados do PITOT!')

            todosOsDados = self.ajudante.receber_dados_usados()

            for cadaDado in todosOsDados:
                for i in range(self.configurador.NUMERO_DE_PITOTS):
                    if cadaDado.apelido == self.ajudante.pitots[i].apelido:
                        self.ajudante.pitots[i].atualiza(cadaDado.getValor(), 1.218)
                        self.criador.pitotTensao[i].setValor(self.ajudante.pitots[i].getValTensao())
                        self.criador.pressaoDin[i].setValor(self.ajudante.pitots[i].getPressaoDinamica("Pa"))
                        self.criador.velCas[i].setValor(self.ajudante.pitots[i].getVelocidade("m/s"))
            time.sleep(delay)


    def atualizarArduino(self, delay):
        """Esta função é utilizada como o processo periódico que
        irá adquirir dados do Arduino.

        :param delay: Valor com o tempo entre cada atualização.
        """
        while self.ajudante.threadsRodando:
            print('Puxando dados do ARDUINO!')

            todosOsDados = self.ajudante.receber_dados_usados()
            dicioDeDados = self.ajudante.arduino.getData()

            for cadaDado in todosOsDados:
                if cadaDado.apelido in dicioDeDados:
                    cadaDado.setValor(dicioDeDados[cadaDado.apelido])


            time.sleep(delay)

    def atualizarCelulas(self, delay):
        """Esta função é utilizada como o processo periódico que
        irá adquirir atualizar os dados de força da balança.

        :param delay: Valor com o tempo entre cada atualização.
        """
        while self.ajudante.threadsRodando:
            print('Puxando dados da Balança!')

            todosOsDados = self.ajudante.receber_dados_usados()

            for cadaDado in todosOsDados:
                for i in range(self.configurador.NUMERO_DE_CELULAS):
                    if cadaDado.apelido == self.ajudante.celulas[i].apelido:
                        self.ajudante.celulas[i].updateForce(cadaDado.getValor())

            time.sleep(delay)

    def atualizarBalanca(self, delay):
        """Esta função é utilizada como o processo periódico que
        irá adquirir atualizar os dados de força da balança.

        :param delay: Valor com o tempo entre cada atualização.
        """
        while self.ajudante.threadsRodando:
            print('Puxando dados da Balança!')

            self.ajudante.balanca.updateForces(self.ajudante.celulas[0].getForce(),
                                                self.ajudante.celulas[1].getForce(),
                                                self.ajudante.celulas[2].getForce(),
                                                self.ajudante.celulas[3].getForce(),
                                                self.ajudante.celulas[4].getForce())

            self.criador.Lift.setValor(self.ajudante.balanca.getLift())
            self.criador.Drag.setValor(self.ajudante.balanca.getDrag())
            self.criador.Moment.setValor(self.ajudante.balanca.getMoment())
            self.criador.DistCp.setValor(self.ajudante.balanca.getDistCp())

            time.sleep(delay)
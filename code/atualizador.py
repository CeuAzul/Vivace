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
            self.criador.mpu.atualiza()
            self.criador.taxaGiroX.setValor(self.criador.mpu.getGyx())
            self.criador.taxaGiroY.setValor(self.criador.mpu.getGyy())
            self.criador.taxaGiroZ.setValor(self.criador.mpu.getGyz())
            self.criador.aceleracaoX.setValor(self.criador.mpu.getAcx())
            self.criador.aceleracaoY.setValor(self.criador.mpu.getAcy())
            self.criador.aceleracaoZ.setValor(self.criador.mpu.getAcz())
            self.criador.pitch.setValor(self.criador.mpu.getPitch())
            self.criador.roll.setValor(self.criador.mpu.getRoll())
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
            self.criador.pressaoEstatica.setValor(self.criador.barometro.getPressao("PA"))
            self.criador.pressaoEstaticar.setValor(self.criador.barometro.getPressao("PA"))
            self.criador.pressaoTotal.setValor(self.criador.barometro.getPressao("PA") + self.criador.pitot.getPressaoDinamica("PA"))
            self.criador.pressaoTotalr.setValor(self.criador.barometro.getPressao("PA") + self.criador.pitot.getPressaoDinamica("PA"))
            self.criador.temperaturaBar.setValor(self.criador.barometro.getTemperatura())
            self.criador.densidadeAr.setValor(self.criador.barometro.getDensidadeAr())
            self.criador.altitudeRelativa.setValor(self.criador.barometro.getAltitudeRelativa("m"))
            self.criador.altitudePressao.setValor(self.criador.barometro.getAltitudePressao("ft"))
            time.sleep(delay)

    def atualizarGps(self, delay):
        """Esta função é utilizada como o processo periódico que
        irá adquirir dados do gps.

        :param delay: Valor com o tempo entre cada atualização.
        """
        while self.ajudante.threadsRodando:
            self.criador.gps.atualiza()
            self.criador.latitude.setValor(self.criador.gps.getLatitude())
            self.criador.longitude.setValor(self.criador.gps.getLongitude())
            self.criador.altitude.setValor(self.criador.gps.getAltitude())
            self.criador.direcaoCurso.setValor(self.criador.gps.getDirecaoCurso())
            self.criador.velocidade.setValor(self.criador.gps.getVelocidade())
            self.criador.velocidadeSubida.setValor(self.criador.gps.getVelSubida())
            self.criador.erroX.setValor(self.criador.gps.getErroX())
            self.criador.erroY.setValor(self.criador.gps.getErroY())
            self.criador.erroAltitude.setValor(self.criador.gps.getErroAltitude())
            self.criador.erroVelocidade.setValor(self.criador.gps.getErroVelocidade())
            self.criador.erroVelocidadeSubida.setValor(self.criador.gps.getErroVelSubida())
            self.criador.nivelFixacao.setValor(self.criador.gps.getNivelFixacao())
            self.criador.latitudeRef.setValor(self.criador.gps.getLatitudeRef())
            self.criador.longitudeRef.setValor(self.criador.gps.getLongitudeRef())
            self.criador.posicaoX.setValor(self.criador.gps.getPosicaoX())
            self.criador.posicaoY.setValor(self.criador.gps.getPosicaoY())
            self.criador.distanciaAbsoluta.setValor(self.criador.gps.getDistanciaAbsoluta())
            self.criador.tempoGps = self.gps.ajudante.getTempo()
            self.criador.dadoTempoGPS.setValor(self.criador.tempoGps)

            agora = datetime.now()
            inicioDia = datetime(agora.year, agora.month, agora.day)

            if (self.criador.gps.verificaAtualizacaoHorario()) and (self.ajudante.modo.getValor() == 0):
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
                self.criador.rawPitotData[i].setValor(self.criador.pitots[i].getRawPitotData())
                self.criador.pressaoDinRef[i].setValor(self.criador.pitots[i].getPressaoDinRef())
                self.criador.velCasRef[i].setValor(self.criador.pitots[i].getVelocidadeRef("m/s"))
            self.criador.velocidadeCarro.setValor(self.criador.pitots[2].getVelocidadeRef("m/s"))
            time.sleep(delay)

    def atualizarSondasAoA(self, delay):
        """Esta função é utilizada como o processo periódico que
        irá adquirir dados das Sondas AoA.

        :param delay: Valor com o tempo entre cada atualização.
        """
        while self.ajudante.threadsRodando:
            for i in range(self.configurador.NUMERO_DE_SONDAS_AOA):
                self.criador.sondas_aoa[i].atualiza(samples=10)
                self.criador.aoa_dif_press[i].setValor(self.criador.sondas_aoa[i].getDifPressure())
                self.criador.aoa_dyn_press[i].setValor(self.criador.sondas_aoa[i].getDynPressure())
                self.criador.aoa[i].setValor(self.criador.sondas_aoa[i].getAoA())
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
                self.criador.rawCellData[i].setValor(self.criador.celulas[i].getRawCellData())
                self.criador.forcas[i].setValor(self.criador.celulas[i].getForce())

            time.sleep(delay)

    def atualizarBalanca(self, delay):
        """Esta função é utilizada como o processo periódico que
        irá adquirir atualizar os dados de força da balança.

        :param delay: Valor com o tempo entre cada atualização.
        """
        while self.ajudante.threadsRodando:
            self.criador.balanca.updateForces(self.criador.forcas[0].getValor(),
                                                self.criador.forcas[1].getValor(),
                                                self.criador.forcas[2].getValor(),
                                                self.criador.forcas[3].getValor(),
                                                self.criador.forcas[4].getValor())

            self.criador.Lift.setValor(self.criador.balanca.getLift())
            self.criador.Drag.setValor(self.criador.balanca.getDrag())
            self.criador.Moment.setValor(self.criador.balanca.getMoment())
            self.criador.DistCp.setValor(self.criador.balanca.getDistCp())

            time.sleep(delay)
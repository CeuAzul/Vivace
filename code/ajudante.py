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

    def atualizarIMU(self, delay):
        """Esta função é utilizada como o processo periódico que
        irá adquirir os dados da IMU.

        :param delay: Valor com o tempo entre cada atualização.
        """
        while self.threadsRodando:
            print('Puxando dados da IMU!')

            self.mpu.atualiza()
            self.taxaGiroX.setValor(self.mpu.getGyx())
            self.taxaGiroY.setValor(self.mpu.getGyy())
            self.taxaGiroZ.setValor(self.mpu.getGyz())
            self.aceleracaoX.setValor(self.mpu.getAcx())
            self.aceleracaoY.setValor(self.mpu.getAcy())
            self.aceleracaoZ.setValor(self.mpu.getAcz())
            self.pitch.setValor(self.mpu.getPitch())
            self.roll.setValor(self.mpu.getRoll())
            time.sleep(delay)


    def atualizarBarometro(self, delay):
        """Esta função é utilizada como o processo periódico que
        irá adquirir dados do barômetro.

        :param delay: Valor com o tempo entre cada atualização.
        """
        while self.threadsRodando:
            print('Puxando dados do BARO!')

            if self.atualizandoReferenciaDoBarometro == True:
                self.barometro.atualizaReferencia()
                atualizaRefBar = False
            self.barometro.atualiza()
            self.pressaoEstatica.setValor(self.barometro.getPressao("PA"))
            self.pressaoEstaticar.setValor(self.barometro.getPressao("PA"))
            self.pressaoTotal.setValor(self.barometro.getPressao("PA") + self.pitot.getPressaoDinamica("PA"))
            self.pressaoTotalr.setValor(self.barometro.getPressao("PA") + self.pitot.getPressaoDinamica("PA"))
            self.temperaturaBar.setValor(self.barometro.getTemperatura())
            self.densidadeAr.setValor(self.barometro.getDensidadeAr())
            self.altitudeRelativa.setValor(self.barometro.getAltitudeRelativa("m"))
            self.altitudePressao.setValor(self.barometro.getAltitudePressao("ft"))
            time.sleep(delay)

    def atualizarGps(self, delay):
        """Esta função é utilizada como o processo periódico que
        irá adquirir dados do gps.

        :param delay: Valor com o tempo entre cada atualização.
        """
        while self.threadsRodando:
            print('Puxando dados do GPS!')

            self.gps.atualiza()
            self.latitude.setValor(self.gps.getLatitude())
            self.longitude.setValor(self.gps.getLongitude())
            self.altitude.setValor(self.gps.getAltitude())
            self.direcaoCurso.setValor(self.gps.getDirecaoCurso())
            self.velocidade.setValor(self.gps.getVelocidade())
            self.velocidadeSubida.setValor(self.gps.getVelSubida())
            self.erroX.setValor(self.gps.getErroX())
            self.erroY.setValor(self.gps.getErroY())
            self.erroAltitude.setValor(self.gps.getErroAltitude())
            self.erroVelocidade.setValor(self.gps.getErroVelocidade())
            self.erroVelocidadeSubida.setValor(self.gps.getErroVelSubida())
            self.nivelFixacao.setValor(self.gps.getNivelFixacao())
            self.latitudeRef.setValor(self.gps.getLatitudeRef())
            self.longitudeRef.setValor(self.gps.getLongitudeRef())
            self.posicaoX.setValor(self.gps.getPosicaoX())
            self.posicaoY.setValor(self.gps.getPosicaoY())
            self.distanciaAbsoluta.setValor(self.gps.getDistanciaAbsoluta())
            self.tempoGps = self.gps.getTempo()
            self.dadoTempoGPS.setValor(self.tempoGps)

            agora = datetime.now()
            inicioDia = datetime(agora.year, agora.month, agora.day)

            if (self.gps.verificaAtualizacaoHorario()) and (self.modo.getValor() == 0):
                self.trocarModoDeTransmissao(1)

            time.sleep(delay)
            self.gps.finaliza()


    def atualizarPitot(self, delay):
        """Esta função é utilizada como o processo periódico que
        irá adquirir dados do pitot.

        :param delay: Valor com o tempo entre cada atualização.
        """
        while self.threadsRodando:
            print('Puxando dados do PITOT!')

            todosOsDados = self.receber_dados_usados()

            for cadaDado in todosOsDados:
                for i in range(self.configurador.NUMERO_DE_PITOTS):
                    if cadaDado.apelido == self.pitots[i].apelido:
                        self.pitots[i].atualiza(cadaDado.getValor(), 1.218)
                        self.pitotTensao[i].setValor(self.pitot.getValTensao())
                        self.pressaoDin[i].setValor(self.pitot.getPressaoDinamica("Pa"))
                        self.velCas[i].setValor(self.pitot.getVelocidade("m/s"))
            time.sleep(delay)


    def atualizarArduino(self, delay):
        """Esta função é utilizada como o processo periódico que
        irá adquirir dados do Arduino.

        :param delay: Valor com o tempo entre cada atualização.
        """
        while self.threadsRodando:
            print('Puxando dados do ARDUINO!')

            todosOsDados = self.receber_dados_usados()
            dicioDeDados = self.arduino.getData()

            for cadaDado in todosOsDados:
                if cadaDado.apelido in dicioDeDados:
                    cadaDado.setValor(dicioDeDados[cadaDado.apelido])


            time.sleep(delay)

    def atualizarCelulas(self, delay):
        """Esta função é utilizada como o processo periódico que
        irá adquirir atualizar os dados de força da balança.

        :param delay: Valor com o tempo entre cada atualização.
        """
        while self.threadsRodando:
            print('Puxando dados da Balança!')

            todosOsDados = self.receber_dados_usados()

            for cadaDado in todosOsDados:
                for i in range(self.configurador.NUMERO_DE_CELULAS):
                    if cadaDado.apelido == self.celulas[i].apelido:
                        self.celulas[i].updateForce(cadaDado.getValor())

            time.sleep(delay)

    def atualizarBalanca(self, delay):
        """Esta função é utilizada como o processo periódico que
        irá adquirir atualizar os dados de força da balança.

        :param delay: Valor com o tempo entre cada atualização.
        """
        while self.threadsRodando:
            print('Puxando dados da Balança!')

            self.balanca.updateForces(self.celulas[0].getForce(),
                                        self.celulas[1].getForce(),
                                        self.celulas[2].getForce(),
                                        self.celulas[3].getForce(),
                                        self.celulas[4].getForce())

            self.Lift.setValor(self.balanca.getLift())
            self.Drag.setValor(self.balanca.getDrag())
            self.Moment.setValor(self.balanca.getMoment())
            self.DistCp.setValor(self.balanca.getDistCp())

            time.sleep(delay)

class Thredeiro (threading.Thread):

    def __init__(self, name, funcaoAlvo, delay):
        threading.Thread.__init__(self, target=funcaoAlvo, args=(delay,))
        print('Thread de ' + name + ' iniciada!')
        self.start()


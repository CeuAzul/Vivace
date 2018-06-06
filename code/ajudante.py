#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
from datetime import datetime
import threading

from libs.datilografo import Escritor
from libs.telepatia import Transmissor
from libs.dado import Dado

from libs.mpu import MPU
from libs.barometro import Barometro
# from libs.gps import Gps
# from libs.pitot import Pitot
from libs.nano import Nano

from configurador import Configurador
# from modos_de_transmissao import SeletorDeModos

class Ajudante(object):

    def __init__(self):
        self.configurador = Configurador()
        # self.seletorDeModos = SeletorDeModos()
        self.telecomandoExecutado = False
        self.threadsRodando = True
        self.inicioDoDia = datetime(datetime.now().year,
                                    datetime.now().month,
                                    datetime.now().day)
        self.tempoAtual = (datetime.now() - self.inicioDoDia).total_seconds()
        self.atualizandoReferenciaDoBarometro = False
        self.NaN = float('nan')
        self.tempoGPS = self.NaN
        self.utc = self.NaN
        self.sensores = ["IMU", "BARO", "GPS", "PITOT", "CELULA"]


    def ativar_sensores(self):
        if self.configurador.USAR_IMU == True:
            print('IMU ativada!')
            # self.mpu = MPU(True, True, True, True, True, True, True, True)
        if self.configurador.USAR_BARO == True:
            print('BARO ativada!')
            # self.barometro = Barometro(True, True)
        if self.configurador.USAR_GPS == True:
            print('GPS ativada!')
            # self.gps = Gps()
        if self.configurador.USAR_PITOTS == True:
            print('PITOTS ativados!')
            # self.pitot = Pitot(0)
        if self.configurador.USAR_NANO == True:
            print('NANO ativada!')
            # self.nano = Nano()
        if self.configurador.USAR_CELULAS == True:
            print('CELULAS ativadas!')
            # self.nano = Nano()


    def criar_dados(self):

        self.tempo = Dado("Tempo", "seg", "tmp", True, True, False, 4)
        self.mensagemRecebida = Dado("Mensagem", "str", "str", True, False, False)
        self.modo = Dado("Modo", "int", "sin", False, True, True)
        self.tamanho = Dado("Tamanho do arquivo", "int", "agr", False, True, True, 3)

        if self.configurador.USAR_IMU == True:
            print('IMU dados criados!')

            self.taxaGiroX = Dado("Taxa de giro em X", "º/s", "gyx", True, False, False, 2, "IMU")
            self.taxaGiroY = Dado("Taxa de giro em Y", "º/s", "gyy", True, False, False, 2, "IMU")
            self.taxaGiroZ = Dado("Taxa de giro em Z", "º/s", "gyz", True, False, False, 2, "IMU")
            self.aceleracaoX = Dado("Aceleração em X", "g", "acx", True, False, False, 2, "IMU")
            self.aceleracaoY = Dado("Aceleração em Y", "g", "acy", True, False, False, 2, "IMU")
            self.aceleracaoZ = Dado("Aceleração em Z", "g", "acz", True, False, False, 2, "IMU")
            self.pitch = Dado("Pitch", "º", "pit", True, False, False, 2, "IMU")
            self.roll = Dado("Roll", "º", "rol", True, False, False, 2, "IMU")

        if self.configurador.USAR_BARO == True:
            print('BARO dados criados!')

            self.pressaoTotal = Dado("Pressao total", "PA", "ptt", True, True, False, 3, "BARO")
            self.pressaoEstatica = Dado("Pressao estática", "PA", "pts", True, True, False, 3, "BARO")
            self.pressaoTotalr = Dado("PTtotal", "PA", "ptt", True, False, False, 3, "BARO")
            self.pressaoEstaticar = Dado("PTstatic", "PA", "psr", True, False, False, 3, "BARO")
            self.temperaturaBar = Dado("Temperatura", "ºC", "tem", True, False, False, 3, "BARO")
            self.densidadeAr = Dado("Densidade do ar", "Kg/m³", "den", True, False, False, 3, "BARO")
            self.altitudeRelativa = Dado("Altitude relativa", "m", "alt", True, False, False, 3, "BARO")
            self.altitudePressao = Dado("HP", "ft", "hps", True, True, False, 3, "BARO")

        if self.configurador.USAR_GPS == True:
            print('GPS dados criados!')

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

        if self.configurador.USAR_PITOTS == True:
            print('PITOT dados criados!')

            nomeDosPitots = self.configurador.NOME_DOS_PITOTS
            apelidoDosPitots = self.configurador.APELIDO_DOS_PITOTS

            self.pressADC = []
            self.pressTensao = []
            self.pressaoDin = []
            self.velCas = []

            for pitot in range(self.configurador.NUMERO_DE_PITOTS):
                print(nomeDosPitots[pitot] + ' criado!')
                self.pressADC.extend([Dado("Valor ADC - " + nomeDosPitots[pitot], "Int", apelidoDosPitots[pitot], False, False, True, 3, "PITOT")])
                self.pressTensao.extend([Dado("Tensao - " + nomeDosPitots[pitot], "V", "ppv_" + apelidoDosPitots[pitot], False, False, False, 6, "PITOT")])
                self.pressaoDin.extend([Dado("Pressao Dinamica - " + nomeDosPitots[pitot], "PA", "ppp_" + apelidoDosPitots[pitot], True, True, False, 3, "PITOT")])
                self.velCas.extend([Dado("VCAS - " + nomeDosPitots[pitot], "m/s", "vcs_" + apelidoDosPitots[pitot], True, True, True, 4, "PITOT")])

        if self.configurador.USAR_CELULAS == True:
            print('CELULAS dados criados!')

            self.forcaH = Dado("Forca - Celula Horizontal ", "kg", "fh", False, False, True, 3, "CELULA")
            self.forcaFD = Dado("Forca - Celula Frontal Direita ", "kg", "ffd", False, False, True, 3, "CELULA")
            self.forcaFE = Dado("Forca - Celula Frontal Esquerda ", "kg", "ffe", False, False, True, 3, "CELULA")
            self.forcaTD = Dado("Forca - Celula Traseira Direita ", "kg", "ftd", False, False, True, 3, "CELULA")
            self.forcaTE = Dado("Forca - Celula Traseira Esquerda ", "kg", "fte", False, False, True, 3, "CELULA")

    def receber_todos_os_dados(self):
        todosOsDados = []

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

        for pitot in range(self.configurador.NUMERO_DE_PITOTS):
            todosOsDados.extend([
                self.pressADC[pitot],
                self.pressTensao[pitot],
                self.pressaoDin[pitot],
                self.velCas[pitot]
            ])

        for celula in range(self.configurador.NUMERO_DE_CELULAS):
            todosOsDados.extend([
                self.forca[celula],
            ])

        return todosOsDados

    def receber_pacote_de_dados(self):

        pacoteDeDados = []
        todosOsDados = self.receber_todos_os_dados()
        for dado in todosOsDados:
            if dado.sensor == "IMU":
                if self.configurador.USAR_IMU == True:
                    pacoteDeDados.extend([dado])
            if dado.sensor == "BARO":
                if self.configurador.USAR_BARO == True:
                    pacoteDeDados.extend([dado])
            if dado.sensor == "GPS":
                if self.configurador.USAR_GPS == True:
                    pacoteDeDados.extend([dado])
            if dado.sensor == "PITOT":
                if self.configurador.USAR_PITOTS == True:
                    pacoteDeDados.extend([dado])
            if dado.sensor == "CELULA":
                if self.configurador.USAR_CELULAS == True:
                    pacoteDeDados.extend([dado])

        return pacoteDeDados

    def ativar_gravacao(self):

        dados = self.receber_pacote_de_dados()
        for dado in dados:
            if dado.sensor == "IMU":
                if self.configurador.GRAVAR_IMU == True:
                    print(dado.nome + ' sendo gravado')
                    dado.setGravacao(True)
            if dado.sensor == "BARO":
                if self.configurador.GRAVAR_BARO == True:
                    print(dado.nome + ' sendo gravado')
                    dado.setGravacao(True)
            if dado.sensor == "GPS":
                if self.configurador.GRAVAR_GPS == True:
                    print(dado.nome + ' sendo gravado')
                    dado.setGravacao(True)
            if dado.sensor == "PITOT":
                if self.configurador.GRAVAR_PITOTS == True:
                    print(dado.nome + ' sendo gravado')
                    dado.setGravacao(True)
            if dado.sensor == "CELULA":
                if self.configurador.GRAVAR_CELULAS == True:
                    print(dado.nome + ' sendo gravada')
                    dado.setGravacao(True)

    def ativar_transmissao(self):
        dados = self.receber_pacote_de_dados()
        for dado in dados:
            if dado.sensor == "IMU":
                if self.configurador.TRANSMITIR_IMU == True:
                    print(dado.nome + ' sendo transmitido')
                    dado.setGravacao(True)
            if dado.sensor == "BARO":
                if self.configurador.TRANSMITIR_BARO == True:
                    print(dado.nome + ' sendo transmitido')
                    dado.setGravacao(True)
            if dado.sensor == "GPS":
                if self.configurador.TRANSMITIR_GPS == True:
                    print(dado.nome + ' sendo transmitido')
                    dado.setGravacao(True)
            if dado.sensor == "PITOT":
                if self.configurador.TRANSMITIR_PITOTS == True:
                    print(dado.nome + ' sendo transmitido')
                    dado.setGravacao(True)
            if dado.sensor == "CELULA":
                if self.configurador.TRANSMITIR_CELULAS == True:
                    print(dado.nome + ' sendo transmitida')
                    dado.setGravacao(True)

    def criar_escritor_transmissor(self):
        print('Escritor e Transmissor criados!')
        self.escritor = Escritor("\t", True, True, "Global - ", ".txt", pasta=self.configurador.PASTA_DESTINO)
        # self.transmissor = Transmissor(",", True, 57600, 'UTF-8')

    def criar_novo_arquivo(self):
        print('Novo arquivo sendo criado!')
        self.escritor
        modoAtual = self.modo.getValor()
        self.trocarModoDeTransmissao(0)
        del self.escritor
        self.escritor = Escritor("\t", True, True, "Dados da Telemetria - ", ".txt")
        self.escritor.setDados(self.receber_pacote_de_dados())
        self.trocarModoDeTransmissao(modoAtual)

    def trocarModoDeTransmissao(self, modo):
        print('Trocando para modo ' + str(modo) + ' de transmissao!')
        self.modo.setValor(modo)
        # seletorDeModos.set

    def liga_threads(self):
        print('Ligando as threads!')
        self.threadsRodando = True

    def desliga_threads(self):
        print('Desligando as threads!')
        self.threadsRodando = False

    def transmitirDados(self, delay):
        print('Transmitindo dados!')
        while self.threadsRodando:
            # self.transmissor.setDados(self.receber_novos_dados)
            # self.transmissor.transmiteLinha()
            time.sleep(delay)

    def gravarDados(self, delay):
        print('Gravando dados!')
        while self.threadsRodando == True:
            self.tempoAtual = (datetime.now() - self.inicioDoDia).total_seconds()
            self.tempo.setValor(self.tempoAtual)
            if self.modo.getValor() == 4:
                self.escritor.setDados(self.receber_pacote_de_dados)
                self.escritor.escreveLinhaDado()
            time.sleep(delay)

    def lerTelecomando(self, delay):
        print('Lendo telecomando!')

        # self.tamanho.setValor(self.escritor.verificaTamanhoArquivo())
        # comandoRecebido = self.transmissor.leLinha()
        # self.mensagemRecebida.setValor(comandoRecebido)
        # if comandoRecebido == "@t#c%$0#1$":
        #     if self.telecomandoExecutado == False:
        #         self.telecomandoExecutado = True
        #         self.trocarModoDeTransmissao(4)
        #     else:
        #         self.telecomandoExecutado = False
        time.sleep(delay)

    def atualizarIMU(self, delay):
        """Esta função é utilizada como o processo periódico que
        irá adquirir os dados da IMU.

        :param delay: Valor com o tempo entre cada atualização.
        """
        print('Puxando dados da IMU!')

        # self.mpu.atualiza()
        # self.taxaGiroX.setValor(self.mpu.getGyx())
        # self.taxaGiroY.setValor(self.mpu.getGyy())
        # self.taxaGiroZ.setValor(self.mpu.getGyz())
        # self.aceleracaoX.setValor(self.mpu.getAcx())
        # self.aceleracaoY.setValor(self.mpu.getAcy())
        # self.aceleracaoZ.setValor(self.mpu.getAcz())
        # self.pitch.setValor(self.mpu.getPitch())
        # self.roll.setValor(self.mpu.getRoll())
        time.sleep(delay)


    def atualizarBarometro(self, delay):
        """Esta função é utilizada como o processo periódico que
        irá adquirir dados do barômetro.

        :param delay: Valor com o tempo entre cada atualização.
        """
        print('Puxando dados do BARO!')

        # if self.atualizandoReferenciaDoBarometro == True:
        #     self.barometro.atualizaReferencia()
        #     atualizaRefBar = False
        # self.barometro.atualiza()
        # self.pressaoEstatica.setValor(self.barometro.getPressao("PA"))
        # self.pressaoEstaticar.setValor(self.barometro.getPressao("PA"))
        # self.pressaoTotal.setValor(self.barometro.getPressao("PA") + self.pitot.getPressaoDinamica("PA"))
        # self.pressaoTotalr.setValor(self.barometro.getPressao("PA") + self.pitot.getPressaoDinamica("PA"))
        # self.temperaturaBar.setValor(self.barometro.getTemperatura())
        # self.densidadeAr.setValor(self.barometro.getDensidadeAr())
        # self.altitudeRelativa.setValor(self.barometro.getAltitudeRelativa("m"))
        # self.altitudePressao.setValor(self.barometro.getAltitudePressao("ft"))
        time.sleep(delay)

    def atualizarGps(self, delay):
        """Esta função é utilizada como o processo periódico que
        irá adquirir dados do gps.

        :param delay: Valor com o tempo entre cada atualização.
        """
        print('Puxando dados do GPS!')

        # self.gps.atualiza()
        # self.latitude.setValor(self.gps.getLatitude())
        # self.longitude.setValor(self.gps.getLongitude())
        # self.altitude.setValor(self.gps.getAltitude())
        # self.direcaoCurso.setValor(self.gps.getDirecaoCurso())
        # self.velocidade.setValor(self.gps.getVelocidade())
        # self.velocidadeSubida.setValor(self.gps.getVelSubida())
        # self.erroX.setValor(self.gps.getErroX())
        # self.erroY.setValor(self.gps.getErroY())
        # self.erroAltitude.setValor(self.gps.getErroAltitude())
        # self.erroVelocidade.setValor(self.gps.getErroVelocidade())
        # self.erroVelocidadeSubida.setValor(self.gps.getErroVelSubida())
        # self.nivelFixacao.setValor(self.gps.getNivelFixacao())
        # self.latitudeRef.setValor(self.gps.getLatitudeRef())
        # self.longitudeRef.setValor(self.gps.getLongitudeRef())
        # self.posicaoX.setValor(self.gps.getPosicaoX())
        # self.posicaoY.setValor(self.gps.getPosicaoY())
        # self.distanciaAbsoluta.setValor(self.gps.getDistanciaAbsoluta())
        # self.tempoGps = self.gps.getTempo()
        # self.dadoTempoGPS.setValor(self.tempoGps)

        # agora = datetime.now()
        # inicioDia = datetime(agora.year, agora.month, agora.day)

        # if (self.gps.verificaAtualizacaoHorario()) and (self.modo.getValor() == 0):
        #     self.trocarModoDeTransmissao(1)

        time.sleep(delay)
        # self.gps.finaliza()


    def atualizarPitot(self, delay):
        """Esta função é utilizada como o processo periódico que
        irá adquirir dados do pitot.

        :param delay: Valor com o tempo entre cada atualização.
        """
        print('Puxando dados do PITOT!')
        # self.pitot.atualiza(20, 1.218)
        # self.pressADC.setValor(self.pitot.getValADC())
        # self.pressTensao.setValor(self.pitot.getValTensao())
        # self.pressaoDin.setValor(self.pitot.getPressaoDinamica("PA"))
        # self.velCas.setValor(self.pitot.getVelocidade("m/s"))
        time.sleep(delay)


    def atualizarNano(self, delay):
        """Esta função é utilizada como o processo periódico que
        irá adquirir dados do nano.

        :param delay: Valor com o tempo entre cada atualização.
        """
        print('Puxando dados do NANO!')

        # todosOsDados = self.receber_todos_os_dados()
        # linhaDeDados = self.nano.receber_linha_de_dados()

        # dados = linhaDeDados.split(';')
        # for dado in dados:
        #     valores = dado.split(',')
        #     apelido = valores[0]
        #     valor = valores[1]

        #     for cadaDado in todosOsDados:
        #         if cadaDado.apelido == apelido:
        #             cadaDado.setValor(valor)


        time.sleep(delay)

class Thredeiro(object):

    def __init__(self, funçaoAlvo, delay):
        print('Thread iniciada!')
        self.thread = threading.Thread(target=funçaoAlvo, args=(delay,))
        self.thread.setDaemon(True)
        self.thread.start()

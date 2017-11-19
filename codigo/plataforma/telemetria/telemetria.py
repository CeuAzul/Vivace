#!/usr/bin/python
# -*- coding: utf-8 -*-

"""FUNÇÃO GLOBAL
Código que cria objeto de todos os sensore e faz com que eles
trabalhem em harmonia usando as threads.

Neste código é utilizado a MPU, Barômetro e o GPS
"""
import time
import os
from datetime import datetime
import threading
from libs.dado import Dado
from libs.mpu import MPU
from libs.datilografo import Escritor
from libs.telepatia import Transmissor
from libs.barometro import Barometro
from libs.gps import Gps
from libs.pitot import Pitot
from libs.nano import Nano

def main():

    NaN = float('nan')


    # Cria objeto dos sensores
    mpu = MPU(True, True, True, True, True, True, True, True)
    barometro = Barometro(True, True)
    gps = Gps()
    pitot8b = Pitot8b(0)
    pitot8bRPMD = Pitot8b(2)
    pitot8bRPME = Pitot8b(3)
    nano = Nano()

    # Cria escritor e transmissor
    escritor = Escritor("\t", True, True, "Global - ", ".txt")
    transmissor = Transmissor(",", True, 57600, 'UTF-8')

    # Dados da MPU
    tempo = Dado("Tempo", "seg", "tmp", True, True, False, 4)
    taxaGiroX = Dado("Taxa de giro em X", "º/s", "gyx", True, False, False, 2)
    taxaGiroY = Dado("Taxa de giro em Y", "º/s", "gyy", True, False, False, 2)
    taxaGiroZ = Dado("Taxa de giro em Z", "º/s", "gyz", True, False, False, 2)
    aceleracaoX = Dado("Aceleração em X", "g", "acx", True, False, False, 2)
    aceleracaoY = Dado("Aceleração em Y", "g", "acy", True, False, False, 2)
    aceleracaoZ = Dado("Aceleração em Z", "g", "acz", True, False, False, 2)
    pitch = Dado("Pitch", "º", "pit", True, False, False, 2)
    roll = Dado("Roll", "º", "rol", True, False, False, 2)

    # Dados do barômetro
    pressaoTotal = Dado("Pressao total", "PA", "ptt", True, True, False, 3)
    pressaoEstatica = Dado("Pressao estática", "PA", "pts", True, True, False, 3)
    pressaoTotalr = Dado("PTtotal", "PA", "ptt", True, False, False, 3)
    pressaoEstaticar = Dado("PTstatic", "PA", "psr", True, False, False, 3)
    temperaturaBar = Dado("Temperatura", "ºC", "tem", True, False, False, 3)
    densidadeAr = Dado("Densidade do ar", "Kg/m³", "den", True, False, False, 3)
    altitudeRelativa = Dado("Altitude relativa", "m", "alt", True, False, False, 3)
    altitudePressao = Dado("HP", "ft", "hps", True, True, False, 3)

    # Dados do Gps
    dadoTempoGPS = Dado("Tempo GPS", "-", "tmg", True, False, False)
    latitude = Dado("Latitude", "º", "lat", True, False, False, 6)
    longitude = Dado("Longitude", "º", "lng", True, False, False, 6)
    altitude = Dado("ZGPS", "m", "atg", True, False, False, 2)
    direcaoCurso = Dado("Direção de curso", "º", "cog", True, False, False, 1)
    velocidade = Dado("Velocidade GPS", "m/s", "vel", True, True, False, 2)
    velocidadeSubida = Dado("Velocidade de subida", "m/s",
                            "ves", False, False, False, 2)
    erroX = Dado("Erro em X", "m", "erx", False, False, False, 1)
    erroY = Dado("Erro em Y", "m", "ery", False, False, False, 1)
    erroAltitude = Dado("Erro da altitude", "m", "era", False, False, False, 1)
    erroVelocidade = Dado("Erro de velocidade", "nós",
                        "ers", False, False, False, 1)
    erroVelocidadeSubida = Dado(
        "Erro da velocidade de subida", "m/s", "ves", False, False, False, 1)
    nivelFixacao = Dado("Nivel de fixação GPS", "-", "nfx", True, False, False, 1)
    latitudeRef = Dado("Latitude de referência", "-", "ltr", False, True, False, 6)
    longitudeRef = Dado("Longitude de referência", "-",
                        "lgr", False, True, False, 6)
    posicaoX = Dado("XGPS", "m", "gpx", True, True, False, 2)
    posicaoY = Dado("YGPS", "m", "gpy", True, True, False, 2)
    distanciaAbsoluta = Dado("Distancia absoluta", "m",
                            "dtr", False, False, False, 2)

    # Dados do pitot
    pressADC = Dado("Valor ADC", "Int", "ppa", False, False, True, 3)
    pressTensao = Dado("Tensao", "V", "ppv", False, False, False, 6)
    pressaoDin = Dado("Pressao Dinamica", "PA", "ppp", True, True, False, 3)
    velCas = Dado("VCAS", "m/s", "vcs", True, True, True, 4)

    # Dados do Nano
    rpmD = Dado("RPM", "rpm", "rpm", True, True, False)
    rpmE = Dado("RPME", "Rpd", "rpd", True, True, False)
    wow = Dado("WOW", "bit", "wow", True, True, False)
    wowRaw = Dado("Wow raw", "bit", "wop", True, False, False)
    tempoVoo = Dado("Tempo de voo", "s", "tpv", False, False, False)
    distancia = Dado("Distância", "cm", "tpv", True, False, False)
    distRef = Dado("Distancia referência", "cm", "dsr", True, False, False)

    # Grava transmissão de mensagem
    ultimoTransmitido = Dado("Mensagem", "str", "str", True, False, False)

    # Variavel para confirmação de telecomando
    teleconfirm = 0

    # Flags de saúde do sistema

    sinaldo = Dado("Sinaldo", "int", "sin", False, True, True)
    # Funcionamento do Sinaldo
    # 0 = Plataforma ligada, sistema calibrando...
    # 1 = Sistema calibrado e horário atualizado, aguardando inicio de gravação...
    # 2 = Apenas transmitindo tempo, Vcas, HP, RPM e altitude(gps)
    # 3 = Apenas transmissão de dados no modo normal
    # 4 = Transmitindo e gravando dados no modo normal

    agravante = Dado("Agravante", "int", "agr", False, True, True, 3)
    # Tamanho do arquivo

    sinaldo.setValor(0)
    tempoGPS = NaN
    utc = NaN

    # Cria indicador para, quando quisermos, parar de executar as threads
    threadsRodando = True


    atualizaRefBar = False
    agora = datetime.now()
    inicioDia = datetime(agora.year, agora.month, agora.day)


    def atualizaVetorDados():
        """Função responsável por atualizar o vetor de dados
        com os dados atualizados pelas funções, vale dizer que essa função
        funciona como se fosse um "empacotador" para poder enviar todos os
        dados ao mesmo tempo para o Escritor e para o Transmissor.

        :returns: Vetor com os dados atualizados com as ultimas aquisições.
        """
        return [tempo,
                wow,
                altitudePressao,
                velCas,
                pressaoEstaticar,
                pressaoTotalr,
                rpmD,
                posicaoX,
                posicaoY,
                altitude,
                rpmE,
                taxaGiroX,
                taxaGiroY,
                taxaGiroZ,
                aceleracaoX,
                aceleracaoY,
                aceleracaoZ,
                pitch,
                roll,
                pressaoEstatica,
                pressaoTotal,
                temperaturaBar,
                densidadeAr,
                altitudeRelativa,
                dadoTempoGPS,
                latitude,
                longitude,
                direcaoCurso,
                velocidade,
                velocidadeSubida,
                erroX,
                erroY,
                erroAltitude,
                erroVelocidade,
                erroVelocidadeSubida,
                nivelFixacao,
                latitudeRef,
                longitudeRef,
                distanciaAbsoluta,
                pressADC,
                pressTensao,
                pressaoDin,
                wowRaw,
                tempoVoo,
                distancia,
                distRef,
                sinaldo,
                agravante,
                ultimoTransmitido]


    def modoDeTransmissao(modo):
        """Função responsável por setar o modo de tranmissao de dados.
        """
        sinaldo.setValor(modo)
        if modo == 0 or modo == 1:
            tempo.setTransmissao(False)
            altitudePressao.setTransmissao(False)
            wow.setTransmissao(False)
            velCas.setTransmissao(False)
            pressaoEstaticar.setTransmissao(False)
            pressaoTotalr.setTransmissao(False)
            rpmD.setTransmissao(False)
            posicaoX.setTransmissao(False)
            posicaoY.setTransmissao(False)
            altitude.setTransmissao(False)
            rpmE.setTransmissao(False)
            taxaGiroX.setTransmissao(False)
            taxaGiroY.setTransmissao(False)
            taxaGiroZ.setTransmissao(False)
            aceleracaoX.setTransmissao(False)
            aceleracaoY.setTransmissao(False)
            aceleracaoZ.setTransmissao(False)
            pitch.setTransmissao(False)
            roll.setTransmissao(False)
            pressaoEstatica.setTransmissao(False)
            pressaoTotal.setTransmissao(False)
            temperaturaBar.setTransmissao(False)
            densidadeAr.setTransmissao(False)
            altitudeRelativa.setTransmissao(False)
            dadoTempoGPS.setTransmissao(False)
            latitude.setTransmissao(False)
            longitude.setTransmissao(False)
            direcaoCurso.setTransmissao(False)
            velocidade.setTransmissao(False)
            velocidadeSubida.setTransmissao(False)
            erroX.setTransmissao(False)
            erroY.setTransmissao(False)
            erroAltitude.setTransmissao(False)
            erroVelocidade.setTransmissao(False)
            erroVelocidadeSubida.setTransmissao(False)
            latitudeRef.setTransmissao(False)
            longitudeRef.setTransmissao(False)
            distanciaAbsoluta.setTransmissao(False)
            pressADC.setTransmissao(False)
            pressTensao.setTransmissao(False)
            pressaoDin.setTransmissao(False)
            wowRaw.setTransmissao(False)
            tempoVoo.setTransmissao(False)
            distancia.setTransmissao(False)
            distRef.setTransmissao(False)
            sinaldo.setTransmissao(True)
            nivelFixacao.setTransmissao(True)
            agravante.setTransmissao(True)
            ultimoTransmitido.setTransmissao(False)
        # 2 = Apenas transmitindo tempo, Vcas, HP, RPM e altitude(gps)
        elif modo == 2:
            tempo.setTransmissao(True)
            altitudePressao.setTransmissao(True)
            wow.setTransmissao(True)
            velCas.setTransmissao(True)
            pressaoEstaticar.setTransmissao(False)
            pressaoTotalr.setTransmissao(False)
            rpmD.setTransmissao(True)
            posicaoX.setTransmissao(False)
            posicaoY.setTransmissao(False)
            altitude.setTransmissao(True)
            rpmE.setTransmissao(True)
            taxaGiroX.setTransmissao(False)
            taxaGiroY.setTransmissao(False)
            taxaGiroZ.setTransmissao(False)
            aceleracaoX.setTransmissao(False)
            aceleracaoY.setTransmissao(False)
            aceleracaoZ.setTransmissao(False)
            pitch.setTransmissao(True)
            roll.setTransmissao(True)
            pressaoEstatica.setTransmissao(False)
            pressaoTotal.setTransmissao(False)
            temperaturaBar.setTransmissao(False)
            densidadeAr.setTransmissao(False)
            altitudeRelativa.setTransmissao(False)
            dadoTempoGPS.setTransmissao(False)
            latitude.setTransmissao(False)
            longitude.setTransmissao(False)
            direcaoCurso.setTransmissao(False)
            velocidade.setTransmissao(False)
            velocidadeSubida.setTransmissao(False)
            erroX.setTransmissao(False)
            erroY.setTransmissao(False)
            erroAltitude.setTransmissao(False)
            erroVelocidade.setTransmissao(False)
            erroVelocidadeSubida.setTransmissao(False)
            latitudeRef.setTransmissao(False)
            longitudeRef.setTransmissao(False)
            distanciaAbsoluta.setTransmissao(False)
            pressADC.setTransmissao(False)
            pressTensao.setTransmissao(False)
            pressaoDin.setTransmissao(False)
            wowRaw.setTransmissao(False)
            tempoVoo.setTransmissao(False)
            distancia.setTransmissao(False)
            distRef.setTransmissao(False)
            sinaldo.setTransmissao(True)
            nivelFixacao.setTransmissao(True)
            agravante.setTransmissao(True)
            ultimoTransmitido.setTransmissao(False)
        elif (modo == 3) or (modo == 4):
            tempo.setTransmissao(True)
            altitudePressao.setTransmissao(True)
            wow.setTransmissao(True)
            velCas.setTransmissao(True)
            pressaoEstaticar.setTransmissao(True)
            pressaoTotalr.setTransmissao(True)
            rpmD.setTransmissao(True)
            posicaoX.setTransmissao(True)
            posicaoY.setTransmissao(True)
            altitude.setTransmissao(True)
            rpmE.setTransmissao(True)
            taxaGiroX.setTransmissao(False)
            taxaGiroY.setTransmissao(False)
            taxaGiroZ.setTransmissao(False)
            aceleracaoX.setTransmissao(False)
            aceleracaoY.setTransmissao(False)
            aceleracaoZ.setTransmissao(False)
            pitch.setTransmissao(True)
            roll.setTransmissao(True)
            pressaoEstatica.setTransmissao(False)
            pressaoTotal.setTransmissao(False)
            temperaturaBar.setTransmissao(False)
            densidadeAr.setTransmissao(False)
            altitudeRelativa.setTransmissao(False)
            dadoTempoGPS.setTransmissao(False)
            latitude.setTransmissao(False)
            longitude.setTransmissao(False)
            direcaoCurso.setTransmissao(False)
            velocidade.setTransmissao(False)
            velocidadeSubida.setTransmissao(False)
            erroX.setTransmissao(False)
            erroY.setTransmissao(False)
            erroAltitude.setTransmissao(False)
            erroVelocidade.setTransmissao(False)
            erroVelocidadeSubida.setTransmissao(False)
            latitudeRef.setTransmissao(False)
            longitudeRef.setTransmissao(False)
            distanciaAbsoluta.setTransmissao(False)
            pressADC.setTransmissao(False)
            pressTensao.setTransmissao(False)
            pressaoDin.setTransmissao(False)
            wowRaw.setTransmissao(False)
            tempoVoo.setTransmissao(False)
            distancia.setTransmissao(False)
            distRef.setTransmissao(False)
            sinaldo.setTransmissao(True)
            nivelFixacao.setTransmissao(True)
            agravante.setTransmissao(True)
            ultimoTransmitido.setTransmissao(False)


    def atualizaEscritor():
        """Função que atualiza os dados do Escritor, com o vetor de dados atualizados.
        """
        d = atualizaVetorDados()
        escritor.setDados(d)


    def transmiteDado(delay):
        """Esta função é utilizada como o processo periódico que
        transmitirá os dados.

        :param delay: Valor com o tempo entre cada atualização de envio.
        """
        while threadsRodando:
            d = atualizaVetorDados()
            transmissor.setDados(d)
            transmissor.transmiteLinha()
            time.sleep(delay)


    def leTelecomando(delay):
        """Esta função irá periodicamente ler o telecomando recebido

        :param delay: Valor com o tempo entre cada atualização.
        """
        global teleconfirm
        global atualizaRefBar
        while threadsRodando:
            agravante.setValor(escritor.verificaTamanhoArquivo())
            receb = transmissor.leLinha()
            ultimoTransmitido.setValor(receb)
            if receb == "@t#c%$0#1$":
                if teleconfirm == 1:
                    teleconfirm = 0
                    # Inicia gravação + recepção normal
                    modoDeTransmissao(4)
                else:
                    teleconfirm = 1

            if receb == "@%&*v##&(@":
                if teleconfirm == 2:
                    teleconfirm = 0
                    # Transmitir apenas Vcas, hp, RPM e altitude gps
                    modoDeTransmissao(2)
                    gps.setReferenciaAqui()
                    gps.resetaAtualizacaoHorario()
                    pitot8b.setReferenciaAqui(20)
                    pitot8bRPMD.setReferenciaAqui(20)
                    pitot8bRPME.setReferenciaAqui(20)
                    atualizaRefBar = True

                    # pitot8bRPMD.setReferenciaAqui(20)
                    # pitot8bRPME.setReferenciaAqui(20)

                else:
                    teleconfirm = 2

            if receb == "&*$$%#!@&_":
                if teleconfirm == 3:
                    teleconfirm = 0
                    modoDeTransmissao(3)
                    # Apenas transmissão
                else:
                    teleconfirm = 3

            if receb == "*)(#$%@!&*":
                if teleconfirm == 4:
                    teleconfirm = 0
                    modoDeTransmissao(0)
                    # Pausa gravação
                else:
                    teleconfirm = 4

            if receb == "AqT%$BNy*(":
                if teleconfirm == 5:
                    teleconfirm = 0
                    # Novo arquivo
                    novoArquivo()
                else:
                    teleconfirm = 5

            if receb == "Tc*B+@F&5v":
                if teleconfirm == 6:
                    teleconfirm = 0
                    escritor.passaProPendrive()
                    # Passa para o pendrive
                else:
                    teleconfirm = 6

            if receb == "!$@f#_a*(%":
                if teleconfirm == 7:
                    teleconfirm = 0
                    os.system('sudo reboot')
                else:
                    teleconfirm = 7

            if receb == "d&y?%(+#((":
                if teleconfirm == 8:
                    teleconfirm = 0
                    os.system('sudo shutdown now')
                else:
                    teleconfirm = 8
            time.sleep(delay)


    def atualizaIMU(delay):
        """Esta função é utilizada como o processo periódico que
        irá adquirir os dados da IMU.

        :param delay: Valor com o tempo entre cada atualização.
        """
        while threadsRodando:
            mpu.atualiza()
            taxaGiroX.setValor(mpu.getGyx())
            taxaGiroY.setValor(mpu.getGyy())
            taxaGiroZ.setValor(mpu.getGyz())
            aceleracaoX.setValor(mpu.getAcx())
            aceleracaoY.setValor(mpu.getAcy())
            aceleracaoZ.setValor(mpu.getAcz())
            pitch.setValor(mpu.getPitch())
            roll.setValor(mpu.getRoll())
            time.sleep(delay)


    def atualizaBarometro(delay):
        """Esta função é utilizada como o processo periódico que
        irá adquirir dados do barômetro.

        :param delay: Valor com o tempo entre cada atualização.
        """
        global atualizaRefBar
        while threadsRodando:
            if atualizaRefBar == True:
                barometro.atualizaReferencia()
                atualizaRefBar = False
            barometro.atualiza()
            pressaoEstatica.setValor(barometro.getPressao("PA"))
            pressaoEstaticar.setValor(barometro.getPressao("PA"))
            pressaoTotal.setValor(barometro.getPressao(
                "PA") + pitot8b.getPressaoDinamica("PA"))
            pressaoTotalr.setValor(barometro.getPressao(
                "PA") + pitot8b.getPressaoDinamica("PA"))
            temperaturaBar.setValor(barometro.getTemperatura())
            densidadeAr.setValor(barometro.getDensidadeAr())
            altitudeRelativa.setValor(barometro.getAltitudeRelativa("m"))
            altitudePressao.setValor(barometro.getAltitudePressao("ft"))
            time.sleep(delay)


    def atualizaGps(delay):
        global inicioDia
        """Esta função é utilizada como o processo periódico que
        irá adquirir dados do gps.

        :param delay: Valor com o tempo entre cada atualização.
        """
        while threadsRodando:
            gps.atualiza()
            latitude.setValor(gps.getLatitude())
            longitude.setValor(gps.getLongitude())
            altitude.setValor(gps.getAltitude())
            direcaoCurso.setValor(gps.getDirecaoCurso())
            velocidade.setValor(gps.getVelocidade())
            velocidadeSubida.setValor(gps.getVelSubida())
            erroX.setValor(gps.getErroX())
            erroY.setValor(gps.getErroY())
            erroAltitude.setValor(gps.getErroAltitude())
            erroVelocidade.setValor(gps.getErroVelocidade())
            erroVelocidadeSubida.setValor(gps.getErroVelSubida())
            nivelFixacao.setValor(gps.getNivelFixacao())
            latitudeRef.setValor(gps.getLatitudeRef())
            longitudeRef.setValor(gps.getLongitudeRef())
            posicaoX.setValor(gps.getPosicaoX())
            posicaoY.setValor(gps.getPosicaoY())
            distanciaAbsoluta.setValor(gps.getDistanciaAbsoluta())
            tempoGps = gps.getTempo()
            dadoTempoGPS.setValor(tempoGps)

            agora = datetime.now()
            inicioDia = datetime(agora.year, agora.month, agora.day)

            if (gps.verificaAtualizacaoHorario()) and (sinaldo.getValor() == 0):
                modoDeTransmissao(1)

            time.sleep(delay)
        gps.finaliza()


    def atualizaPitot(delay):
        """Esta função é utilizada como o processo periódico que
        irá adquirir dados do pitot.

        :param delay: Valor com o tempo entre cada atualização.
        """
        while threadsRodando:
            pitot8b.atualiza(20, 1.218)
            pressADC.setValor(pitot8b.getValADC())
            pressTensao.setValor(pitot8b.getValTensao())
            pressaoDin.setValor(pitot8b.getPressaoDinamica("PA"))
            velCas.setValor(pitot8b.getVelocidade("m/s"))
            time.sleep(delay)


    def atualizaNano(delay):
        """Esta função é utilizada como o processo periódico que
        irá adquirir dados do nano.

        :param delay: Valor com o tempo entre cada atualização.
        """
        while threadsRodando:
            pitot8bRPMD.atualiza(20, 1.218)
            pitot8bRPME.atualiza(20, 1.218)
            nano.atualiza()
            rpmD.setValor(pitot8bRPMD.getVelocidade())
            rpmE.setValor(pitot8bRPME.getVelocidade())
            wow.setValor(nano.getWow())
            wowRaw.setValor(nano.getWowRaw())
            tempoVoo.setValor(nano.getTempoVoo())
            distancia.setValor(nano.getDistancia())
            distRef.setValor(nano.getDistRef())
            time.sleep(delay)


    def fazCabecalho():
        """Função que manda o comando para gerar o cabeçalho no arquivo de texto.
        Nisso, o arquivo colocará o nome do dado na primeira linha e a unidade de
        medida na segunda linha (caso o usuário tenha decidido isso na criação do Escritor).
        """
        atualizaEscritor()
        escritor.fazCabecalho()


    def novoArquivo():
        """Função cria um novo arquivo de dados caso for chamada.
        """
        global escritor
        modoAtual = sinaldo.getValor()
        modoDeTransmissao(0)
        del escritor
        escritor = Escritor("\t", True, True, "Global - ", ".txt")
        fazCabecalho()
        modoDeTransmissao(modoAtual)


    fazCabecalho()
    tempoAgora = (datetime.now() - inicioDia).total_seconds()


    def atualizaLinhaEscritor(delay):
        """Esta função é utilizada como o processo periódico que
        escrever uma linha de dado no arquivo, utilizando o objeto Escritor.

        :param delay: Valor com o tempo entre cada atualização.
        """
        while threadsRodando:
            tempoAgora = (datetime.now() - inicioDia).total_seconds()
            tempo.setValor(tempoAgora)
            if sinaldo.getValor() == 4:
                atualizaEscritor()
                escritor.escreveLinhaDado()
            time.sleep(delay)


    modoDeTransmissao(0)

    # Inicializa thread de transmissão
    tTransmit = threading.Thread(target=transmiteDado, args=(0.5,))
    tTransmit.setDaemon(True)
    tTransmit.start()

    # Inicializa thread da MPU
    tMpu = threading.Thread(target=atualizaIMU, args=(0.03,))
    tMpu.setDaemon(True)
    tMpu.start()

    # Inicializa thread do barômetro
    tBarometro = threading.Thread(target=atualizaBarometro, args=(0.1,))
    tBarometro.setDaemon(True)
    tBarometro.start()

    # Inicializa thread do GPS
    tGps = threading.Thread(target=atualizaGps, args=(0.5,))
    tGps.setDaemon(True)
    tGps.start()

    # Inicializa thread do Pitot
    tPitot = threading.Thread(target=atualizaPitot, args=(0.2,))
    tPitot.setDaemon(True)
    tPitot.start()

    # Inicializa thread do Nano
    tNano = threading.Thread(target=atualizaNano, args=(0.5,))
    tNano.setDaemon(True)
    tNano.start()

    # Inicializa thread de escrita do dado no arquivo
    tLinhaDado = threading.Thread(target=atualizaLinhaEscritor, args=(0.02,))
    tLinhaDado.setDaemon(True)
    tLinhaDado.start()

    # Inicializa thread de escrita do dado no arquivo
    tTelecomando = threading.Thread(target=leTelecomando, args=(1,))
    tTelecomando.setDaemon(True)
    tTelecomando.start()


    def f():
        """Função finaliza as threads.
        """
        threadsRodando = False

if __name__ == '__main__':

    main()

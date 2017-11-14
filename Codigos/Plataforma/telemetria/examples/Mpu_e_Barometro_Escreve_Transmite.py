"""FUNÇÃO GLOBAL
Código que cria objeto de todos os sensore e faz com que eles
trabalhem em harmonia usando as threads.

Neste código é utilizado a MPU e Barômetro
"""
#!/usr/bin/python
import time
import threading
from lib.dado import Dado
from lib.mpulib import MPU
from lib.datilografo import Escritor
from lib.telepatia import Transmissor
from lib.barometrolib import Barometro

# Cria objeto dos sensores
mpu = MPU(True, True, True, True, True, True, True, True)
barometro = Barometro(True, True)

# Cria escritor e transmissor
escritor = Escritor(",", True, True, "Global - ", ".csv")
transmissor = Transmissor(",", True, 57600, 'UTF-8')

# Dados da MPU
item = Dado("Item", "it", "itn", True, False, False)
tempo = Dado("Tempo", "Segundos", "tmp", True, True, False)
taxaGiroX = Dado("Taxa de giro em X", "º/s", "gyx", True, False, False)
taxaGiroY = Dado("Taxa de giro em Y", "º/s", "gyy", True, False, False)
taxaGiroZ = Dado("Taxa de giro em Z", "º/s", "gyz", True, False, False)
aceleracaoX = Dado("Aceleração em X", "g", "acx", True, False, False)
aceleracaoY = Dado("Aceleração em Y", "g", "acy", True, False, False)
aceleracaoZ = Dado("Aceleração em Z", "g", "acz", True, True, False)
pitch = Dado("Pitch", "º", "pit", True, False, False)
roll = Dado("Roll", "º", "rol", True, False, False)

# Dados do barômetro
pressao = Dado("Pressao real", "pa", "prr", True, True, False)
temperaturaBar = Dado("Temperatura", "ºC", "tem", True, True, False)
densidadeAr = Dado("Densidade do ar", "n lembro", "den", True, True, False)
altitudeRelativa = Dado("Altitude relativa", "m", "alt", True, True, False)
altitudePressao = Dado("Altitude Pressão", "m", "hps", True, True, False)

# Cria indicador para, quando quisermos, parar de executar as threads
threadsRodando = True

inicio = int(round(time.time() * 1000))


def atualizaVetorDados():
    """Função responsável por atualizar o vetor de dados
    com os dados atualizados pelas funções, vale dizer que essa função
    funciona como se fosse um "empacotador" para poder enviar todos os
    dados ao mesmo tempo para o Escritor e para o Transmissor.

    :returns: Vetor com os dados atualizados com as ultimas aquisições.
    """
    return [tempo,
            item,
            taxaGiroX,
            taxaGiroY,
            taxaGiroZ,
            aceleracaoX,
            aceleracaoY,
            aceleracaoZ,
            pitch,
            roll,
            pressao,
            temperaturaBar,
            densidadeAr,
            altitudeRelativa,
            altitudePressao]


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
    while threadsRodando:
        barometro.atualiza()
        pressao.setValor(barometro.getPressao())
        temperaturaBar.setValor(barometro.getTemperatura())
        densidadeAr.setValor(barometro.getDensidadeAr())
        altitudeRelativa.setValor(barometro.getAltitudeRelativa())
        altitudePressao.setValor(barometro.getAltitudePressao())
        time.sleep(delay)


def fazCabecalho():
    """Função que manda o comando para gerar o cabeçalho no arquivo de texto.
    Nisso, o arquivo colocará o nome do dado na primeira linha e a unidade de
    medida na segunda linha (caso o usuário tenha decidido isso na criação do Escritor).
    """
    atualizaEscritor()
    escritor.fazCabecalho()


fazCabecalho()

tempoAgora = int(round(time.time() * 1000)) - inicio
item.setValor(0)


def atualizaLinhaEscritor(delay):
    """Esta função é utilizada como o processo periódico que
    escrever uma linha de dado no arquivo, utilizando o objeto Escritor.

    :param delay: Valor com o tempo entre cada atualização.
    """
    while threadsRodando:
        tempoAgora = int(round(time.time() * 1000)) - inicio
        tempo.setValor(tempoAgora)
        item.setValor(item.getValor() + 1)
        atualizaEscritor()
        escritor.escreveLinhaDado()



# Inicializa thread de transmissão
tTransmit = threading.Thread(target=transmiteDado, args=(0.05,))
tTransmit.setDaemon(True)
tTransmit.start()

# Inicializa thread da MPU
tMpu = threading.Thread(target=atualizaIMU, args=(0.001,))
tMpu.setDaemon(True)
tMpu.start()

# Inicializa thread do barômetro
tBarometro = threading.Thread(target=atualizaBarometro, args=(0.01,))
tBarometro.setDaemon(True)
tBarometro.start()

# Inicializa thread de escrita do dado no arquivo
tLinhaDado = threading.Thread(target=atualizaLinhaEscritor, args=(0.001,))
tLinhaDado.setDaemon(True)
tLinhaDado.start()


def finalizaThreads():
    """Função finaliza as threads.
    """
    threadsRodando = False

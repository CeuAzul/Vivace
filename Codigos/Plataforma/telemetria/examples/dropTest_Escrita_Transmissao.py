"""FUNÇÃO GLOBAL
Código utilizado para realização de droptest.
"""
#!/usr/bin/python
import time
import threading
from lib.dado import Dado
from lib.mpulib import MPU
from lib.datilografo import Escritor
from lib.telepatia import Transmissor

# Cria objeto da MPU e utiliza apenas aceleração
mpu = MPU(False, False, False, True, True, True, False, False)

# Cria objeto do transmissor e do escritor
escritor = Escritor(",", True, True, "Aceleração - ", ".csv")
transmissor = Transmissor(",", True, 57600, 'UTF-8')

# Cria Dados
item = Dado("Item", "it", "itn", True, False, False)
tempo = Dado("Tempo", "Segundos", "tmp", True, True, False)
taxaGiroX = Dado("Taxa de giro em X", "º/s", "gyx", True, False, False)
taxaGiroY = Dado("Taxa de giro em Y", "º/s", "gyy", True, False, False)
taxaGiroZ = Dado("Taxa de giro em Z", "º/s", "gyz", True, False, False)
aceleracaoX = Dado("Aceleração em X", "g", "acx", False, False, False)
aceleracaoY = Dado("Aceleração em Y", "g", "acy", False, False, False)
aceleracaoZ = Dado("Aceleração em Z", "g", "acz", True, True, False)
pitch = Dado("Pitch", "º", "pit", True, False, False)
roll = Dado("Roll", "º", "rol", True, False, False)

inicio = int(round(time.time() * 1000))


def atualizaEscritor():
    """Função que atualiza os dados do Escritor, com o vetor de dados atualizados.
    """
    d = [tempo, item, taxaGiroX, taxaGiroY, taxaGiroZ,
         aceleracaoX, aceleracaoY, aceleracaoZ, pitch, roll]
    escritor.setDados(d)


def transmiteDado(delay):
    """Esta função é utilizada como o processo periódico que
    transmitirá os dados.

    :param delay: Valor com o tempo entre cada atualização de envio.
    """
    while True:
        d = [tempo, item, taxaGiroX, taxaGiroY, taxaGiroZ,
             aceleracaoX, aceleracaoY, aceleracaoZ, pitch, roll]
        transmissor.setDados(d)
        transmissor.transmiteLinha()
        time.sleep(delay)


def atualizaIMU():
    """Esta função é utilizada como o processo periódico que
    irá adquirir os dados da IMU.

    :param delay: Valor com o tempo entre cada atualização.
    """
    mpu.atualiza()
    taxaGiroX.setValor(mpu.getGyx())
    taxaGiroY.setValor(mpu.getGyy())
    taxaGiroZ.setValor(mpu.getGyz())
    aceleracaoX.setValor(mpu.getAcx())
    aceleracaoY.setValor(mpu.getAcy())
    aceleracaoZ.setValor(mpu.getAcz())
    pitch.setValor(mpu.getPitch())
    roll.setValor(mpu.getRoll())


# Atualiza escritor para receber o nome dos dados (para colocar no cabeçalho)
atualizaEscritor()

# Faz cabeçalho
escritor.fazCabecalho()
tempoAgora = int(round(time.time() * 1000)) - inicio
item.setValor(0)

# Cria thread de transmissão
t = threading.Thread(target=transmiteDado, args=(0.1,))
t.setDaemon(True)
t.start()

# Faz processo de aquisição de dado e escrita de linha
while True:
    try:
        atualizaIMU()
        item.setValor(item.getValor() + 1)
        tempoAgora = int(round(time.time() * 1000)) - inicio
        tempo.setValor(tempoAgora)
        atualizaEscritor()
        escritor.escreveLinhaDado()
    except KeyboardInterrupt:
        t.join(1)
        t.kill_received = True
        print("saiu")
        exit()

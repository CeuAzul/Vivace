"""FUNÇÃO GLOBAL
Código exemplo de utilização da biblioteca MPU (escrita de arquivo e transmissão dos dados)
"""
#!/usr/bin/python
import time
import threading
from lib.dado import Dado
from lib.mpulib import MPU
from lib.datilografo import Escritor
from lib.telepatia import Transmissor

# Cria objeto da MPU
mpu = MPU(True, True, True, True, True, True, True, True)

# Cria escritor e transmissor
escritor = Escritor(",", True, True, "Aceleração - ", ".csv")
transmissor = Transmissor(",", True, 57600, 'UTF-8')

# Cria objeto dos dados
item = Dado("Item", "it", "itn", True, False, False)
tempo = Dado("Tempo", "Segundos", "tmp", True, True, False)
taxaGiroX = Dado("Taxa de giro em X", "º/s", "gyx", True, False, False)
taxaGiroY = Dado("Taxa de giro em Y", "º/s", "gyy", True, False, False)
taxaGiroZ = Dado("Taxa de giro em Z", "º/s", "gyz", True, False, False)
aceleracaoX = Dado("Aceleração em X", "g", "acx", True, False, False)
aceleracaoY = Dado("Aceleração em Y", "g", "acy", True, False, False)
aceleracaoZ = Dado("Aceleração em Z", "g", "acz", True, True, False)
pitch = Dado("Pitch", "º", "pit", True, True, False)
roll = Dado("Roll", "º", "rol", True, True, False)

inicio = int(round(time.time() * 1000))


def atualizaEscritor():
    """Função que atualiza os dados do Escritor, com o vetor de dados atualizados.
    """
    d = [tempo, item, taxaGiroX, taxaGiroY, taxaGiroZ,
         aceleracaoX, aceleracaoY, aceleracaoZ, pitch, roll]
    escritor.setDados(d)


def transmiteDado(delay):
    """Função periódica que irá transmitir os dados.
    A função atualiza o vetor de dados do transmissor e transmite os dados selecionados
    """
    while True:
        d = [tempo, item, taxaGiroX, taxaGiroY, taxaGiroZ,
             aceleracaoX, aceleracaoY, aceleracaoZ, pitch, roll]
        transmissor.setDados(d)
        transmissor.transmiteLinha()
        time.sleep(delay)


def atualizaIMU():
    """Função que atualiza os dados da IMU e passa para as variáveis do código global.
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


# Faz cabeçalho
atualizaEscritor()
escritor.fazCabecalho()

tempoAgora = int(round(time.time() * 1000)) - inicio
item.setValor(0)

# Cria thread de transmisão de dados
t = threading.Thread(target=transmiteDado, args=(0.05,))
t.setDaemon(True)
t.start()

# Código periódico responsável por gravar os dados no arquivo e atualizar a IMU
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

"""FUNÇÃO GLOBAL
Código exemplo de utilização da biblioteca MPU (e escrita de arquivo com os dados)
"""
#!/usr/bin/python
import time
from lib.dado import Dado
from lib.mpulib import MPU
from lib.datilografo import Escritor

# Cria objeto da MPU
mpu = MPU(False, False, False, False, False, True, False, False, True)

# Cria escritor
escritor = Escritor(",", True, True, "Aceleração - ", ".csv")

# Cria objeto dos dados
item = Dado("Item", "it", "itn", True, True, False)
tempo = Dado("Tempo", "Segundos", "tmp", True, True, False)
taxaGiroX = Dado("Taxa de giro em X", "º/s", "gyx", True, True, False)
taxaGiroY = Dado("Taxa de giro em Y", "º/s", "gyy", True, True, False)
taxaGiroZ = Dado("Taxa de giro em Z", "º/s", "gyz", True, True, False)
aceleracaoX = Dado("Aceleração em X", "g", "acx", True, True, False)
aceleracaoY = Dado("Aceleração em Y", "g", "acy", True, True, False)
aceleracaoZ = Dado("Aceleração em Z", "g", "acz", True, True, False)
pitch = Dado("Pitch", "º", "pit", True, True, False)
roll = Dado("Roll", "º", "rol", True, True, False)
temperaturaMPU = Dado("Temperatura", "Cº", "tem", True, True, False)


inicio = int(round(time.time() * 1000))


def atualizaEscritor():
    """Função que atualiza os dados do Escritor, com o vetor de dados atualizados.
    """
    d = [item, tempo, taxaGiroX, taxaGiroY, taxaGiroZ, aceleracaoX,
         aceleracaoY, aceleracaoZ, pitch, roll, temperaturaMPU]
    escritor.setDados(d)


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
    temperaturaMPU.setValor(mpu.getTemp())


# Faz cabeçalho
atualizaEscritor()
escritor.fazCabecalho()

tempoAgora = int(round(time.time() * 1000)) - inicio
item.setValor(0)

# Realiza iterações de atualização da IMU e escreve eles no arquivo
while tempoAgora <= 5000:
    atualizaIMU()
    item.setValor(item.getValor() + 1)
    tempoAgora = int(round(time.time() * 1000)) - inicio
    tempo.setValor(tempoAgora)
    atualizaEscritor()
    escritor.escreveLinhaDado()

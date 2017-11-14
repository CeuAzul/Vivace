"""FUNÇÃO GLOBAL
Código que cria objeto de todos os sensore e faz com que eles
trabalhem em harmonia usando as threads.

Neste código é utilizado a MPU, Barômetro e o GPS
"""
#!/usr/bin/python
import time
from datetime import datetime
import threading
from lib.dado import Dado
from lib.mpulib import MPU
from lib.datilografo import Escritor
from lib.telepatia import Transmissor
from lib.barometrolib import Barometro
from lib.gpslib import Gps
NaN = float('nan')

#Cria objeto dos sensores
mpu = MPU(True, True, True, True, True, True, True, True)
barometro = Barometro(True, True)
gps = Gps()

## Cria escritor e transmissor
escritor = Escritor(",", True, True, "Global - ", ".csv")
transmissor = Transmissor(",", True, 57600, 'UTF-8')

## Dados da MPU
tempo = Dado("Tempo", "seg", "tmp", True, True, False)
taxaGiroX = Dado("Taxa de giro em X", "º/s", "gyx", True, False, False)
taxaGiroY = Dado("Taxa de giro em Y", "º/s", "gyy", True, False, False)
taxaGiroZ = Dado("Taxa de giro em Z", "º/s", "gyz", True, False, False)
aceleracaoX = Dado("Aceleração em X", "g", "acx", True, False, False)
aceleracaoY = Dado("Aceleração em Y", "g", "acy", True, False, False)
aceleracaoZ = Dado("Aceleração em Z", "g", "acz", True, False, False)
pitch = Dado("Pitch", "º", "pit", True, False, False)
roll = Dado("Roll", "º", "rol", True, False, False)

## Dados do barômetro
pressaoTotal = Dado("Pressao total", "PA", "ptt", True, True, False)
pressaoEstatica = Dado("Pressao estática", "PA", "pts", True, True, False)
pressaoTotalr = Dado("Pressao total (raw)", "V", "ptt", False, False, False)
pressaoEstaticar = Dado("Pressao estática (raw)", "PA", "psr", True, False, False)
temperaturaBar = Dado("Temperatura", "ºC", "tem", True, False, False)
densidadeAr = Dado("Densidade do ar", "Kg/m³", "den", True, False, False)
altitudeRelativa = Dado("Altitude relativa", "m", "alt", True, False, False)
altitudePressao = Dado("Altitude Pressão", "ft", "hps", True, True, False)

## Dados do Gps
dadoTempoGPS = Dado("Tempo GPS", "-", "tmg", True, False, False)
latitude = Dado("Latitude", "º", "lat", True, False, False)
longitude = Dado("Longitude", "º", "lng", True, False, False)
altitude = Dado("Altitude", "m", "atg", True, False, False)
direcaoCurso = Dado("Direção de curso", "º", "cog", True, False, False)
velocidade = Dado("Velocidade GPS", "nós", "vel", True, True, False)
velocidadeSubida = Dado("Velocidade de subida", "m/s", "ves", True, False, False)
erroX = Dado("Erro em X", "m", "erx", True, False, False)
erroY = Dado("Erro em Y", "m", "ery", True, False, False)
erroAltitude = Dado("Erro da altitude", "m", "era", True, False, False)
erroVelocidade = Dado("Erro de velocidade", "nós", "ers", True, False, False)
erroVelocidadeSubida = Dado("Erro da velocidade de subida", "m/s", "ves", True, False, False)
nivelFixacao = Dado("Nivel de fixação GPS", "-", "mfx", True, False, False)
latitudeRef = Dado("Latitude de referência", "-", "ltr", True, True, False)
longitudeRef = Dado("Longitude de referência", "-", "lgr", True, True, False)
posicaoX = Dado("Posição X", "m", "gpx", True, True, False)
posicaoY = Dado("Posição Y", "m", "gpy", True, True, False)
distanciaAbsoluta = Dado("Distancia absoluta", "m", "dtr", True, False, False)

tempoGPS = NaN
utc = NaN

#Cria indicador para, quando quisermos, parar de executar as threads
threadsRodando = True  

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
         taxaGiroX,
         taxaGiroY,
         taxaGiroZ,
         aceleracaoX,
         aceleracaoY,
         aceleracaoZ,
         pitch,
         roll,
         pressaoTotal,
         pressaoEstatica,
         pressaoTotalr,
         pressaoEstaticar,
         temperaturaBar,
         densidadeAr,
         altitudeRelativa,
         altitudePressao,
         dadoTempoGPS,
         latitude,
         longitude,
         altitude,
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
         posicaoX,
         posicaoY,
         distanciaAbsoluta]

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
        pressaoEstatica.setValor(barometro.getPressao("PA"))
        pressaoEstaticar.setValor(barometro.getPressao("PA"))
        pressaoTotal.setValor(barometro.getPressao("PA"))
        pressaoTotalr.setValor(barometro.getPressao("PA"))
        temperaturaBar.setValor(barometro.getTemperatura())
        densidadeAr.setValor(barometro.getDensidadeAr())
        altitudeRelativa.setValor(barometro.getAltitudeRelativa("ft"))
        altitudePressao.setValor(barometro.getAltitudePressao("ft"))
        time.sleep(delay)

def atualizaGps(delay):
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
        time.sleep(delay)
    gps.finaliza()
        
def fazCabecalho():
    """Função que manda o comando para gerar o cabeçalho no arquivo de texto.
    Nisso, o arquivo colocará o nome do dado na primeira linha e a unidade de
    medida na segunda linha (caso o usuário tenha decidido isso na criação do Escritor). 
    """
    atualizaEscritor()
    escritor.fazCabecalho()

fazCabecalho()
tempoAgora = (datetime.now()-inicioDia).total_seconds()

def atualizaLinhaEscritor(delay):
    """Esta função é utilizada como o processo periódico que
    escrever uma linha de dado no arquivo, utilizando o objeto Escritor.
    
    :param delay: Valor com o tempo entre cada atualização.
    """
    while threadsRodando:
        tempoAgora = (datetime.now()-inicioDia).total_seconds()
        tempo.setValor(tempoAgora)
        atualizaEscritor()
        escritor.escreveLinhaDado()



#Inicializa thread de transmissão
tTransmit = threading.Thread(target=transmiteDado, args=(0.5,))
tTransmit.setDaemon(True)
tTransmit.start()

#Inicializa thread da MPU
tMpu = threading.Thread(target=atualizaIMU, args=(0.01,))
tMpu.setDaemon(True)
tMpu.start()

#Inicializa thread do barômetro
tBarometro = threading.Thread(target=atualizaBarometro, args=(0.01,))
tBarometro.setDaemon(True)
tBarometro.start()

#Inicializa thread do GPS
tGps = threading.Thread(target=atualizaGps, args=(0.3,))
tGps.setDaemon(True)
tGps.start()

#Inicializa thread de escrita do dado no arquivo
tLinhaDado = threading.Thread(target=atualizaLinhaEscritor, args=(0.02,))
tLinhaDado.setDaemon(True)
tLinhaDado.start()

def f():
    """Função finaliza as threads.
    """
    threadsRodando = False



        
            

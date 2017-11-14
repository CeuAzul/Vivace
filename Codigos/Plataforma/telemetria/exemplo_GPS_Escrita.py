"""FUNÇÃO GLOBAL
Código exemplo de utilização da biblioteca do GPS (e escrita de arquivo com os dados)
"""
#!/usr/bin/python
import time
from lib.dado import Dado
from lib.gpslib import Gps
from lib.datilografo import Escritor
import datetime

NaN = float('nan')

#Cria objeto do GPS e do Escritor
gps = Gps()
escritor = Escritor(",", True, True, "GPS - ", ".csv")

#Cria Objeto dos dados
item = Dado("Item", "it", "itn", True, True, False)
tempo = Dado("Tempo", "Segundos", "tmp", True, True, False)
dadoTempoGPS = Dado("Tempo GPS", "-", "tmg", True, True, False)

latitude = Dado("Latitude", "º", "lat", True, True, False)
longitude = Dado("Longitude", "º", "lng", True, True, False)
altitude = Dado("Altitude", "m", "alt", True, True, False)
direcaoCurso = Dado("Direção de curso", "º", "cog", True, True, False)
velocidade = Dado("Velocidade GPS", "nós", "vel", True, True, False)
velocidadeSubida = Dado("Velocidade de subida", "m/s", "ves", True, True, False)

erroX = Dado("Erro em X", "m", "erx", True, True, False)
erroY = Dado("Erro em Y", "m", "ery", True, True, False)
erroAltitude = Dado("Erro da altitude", "m", "era", True, True, False)
erroVelocidade = Dado("Erro de velocidade", "nós", "ers", True, True, False)
erroVelocidadeSubida = Dado("Erro da velocidade de subida", "m/s", "ves", True, True, False)

nivelFixacao = Dado("Nivel de fixação GPS", "-", "mfx", True, True, False)
latitudeRef = Dado("Latitude de referência", "-", "ltr", True, True, False)
longitudeRef = Dado("Longitude de referência", "-", "lgr", True, True, False)

posicaoX = Dado("Posição X", "m", "gpx", True, True, False)
posicaoY = Dado("Posição Y", "m", "gpy", True, True, False)
distanciaAbsoluta = Dado("Distancia absoluta", "m", "dtr", True, True, False)


tempoGPS = NaN
utc = NaN                           

inicio = int(round(time.time()*1000))


def atualizaEscritor():
    """Função que atualiza os dados do Escritor, com o vetor de dados atualizados.
    """
    d = [tempo, dadoTempoGPS, item, latitude, longitude, altitude, direcaoCurso, velocidade, velocidadeSubida, erroX, erroY, erroAltitude, erroVelocidade, erroVelocidadeSubida, nivelFixacao, latitudeRef, longitudeRef, posicaoX, posicaoY, distanciaAbsoluta]
    escritor.setDados(d)

def atualizaGps():
    """Função adquire os dados do GPS e passa eles para as variáveis
    do código global.
    """
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

#Faz cabeçalho
atualizaEscritor()
escritor.fazCabecalho()

tempoAgora = int(round(time.time()*1000)) - inicio
item.setValor(0)
print("calibrou")

#Faz iterações de atualizações do gps e escrita dos dados no arquivo
while tempoAgora <= 600000 :
    atualizaGps()
    item.setValor(item.getValor()+1)
    tempoAgora = int(round(time.time()*1000)) - inicio
    tempo.setValor(tempoAgora)
    atualizaEscritor()
    escritor.escreveLinhaDado()
    print(nivelFixacao.getValor() , " , " , dadoTempoGPS.getValor(), " , ", gps.getUTC())


    time.sleep(0.1)
gps.finaliza()

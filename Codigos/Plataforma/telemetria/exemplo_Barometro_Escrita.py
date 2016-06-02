"""
FUNÇÃO GLOBAL
Código exemplo de utilização da biblioteca do barômetro
"""
#!/usr/bin/python
import time
from lib.dado import Dado
from lib.barometrolib import Barometro
from lib.datilografo import Escritor

#Cria o dado do barômetro
barometro = Barometro(True, True)

#Cria objeto do escritor
escritor = Escritor(",", True, True, "Barometro - ", ".csv")

#Cria objeto dos dados
item = Dado("Item", "it", "itn", True, True, False)
tempo = Dado("Tempo", "Segundos", "tmp", True, True, False)
pressao = Dado("Pressao real", "pa", "prr", True, True, False)
temperaturaBar = Dado("Temperatura", "ºC", "tem", True, True, False)
densidadeAr = Dado("Densidade do ar", "n lembro", "den", True, True, False)
altitudeRelativa = Dado("Altitude relativa", "m", "alt", True, True, False)
altitudePressao = Dado("Altitude Pressão", "m", "hps", True, True, False)


inicio = int(round(time.time()*1000))

def atualizaEscritor():
    """Atualiza vetor de dados e passa eles para o Escritor.
    """
    d = [item, tempo, pressao, temperaturaBar, densidadeAr, altitudeRelativa, altitudePressao]
    escritor.setDados(d)

def atualizaBarometro():
    """Atualiza dados do barômetro e pega parâmetros e coloca nas variáveis.
    """
    barometro.atualiza()
    pressao.setValor(barometro.getPressao())
    temperaturaBar.setValor(barometro.getTemperatura())
    densidadeAr.setValor(barometro.getDensidadeAr())
    altitudeRelativa.setValor(barometro.getAltitudeRelativa())
    altitudePressao.setValor(barometro.getAltitudePressao())


#Faz cabeçalho no arquivo
atualizaEscritor()
escritor.fazCabecalho()

tempoAgora = int(round(time.time()*1000)) - inicio
item.setValor(0)

#Faz iterações de atualizações e escritas de arquivo.
while tempoAgora <= 5000 :
    atualizaBarometro()
    item.setValor(item.getValor()+1)
    tempoAgora = int(round(time.time()*1000)) - inicio
    tempo.setValor(tempoAgora)
    atualizaEscritor()
    escritor.escreveLinhaDado()
  ##  print("Pressão: ", barometro.getPressao(), "  Temp: ", barometro.getTemperatura(), "   Dens: ", barometro.getDensidadeAr(), "   Alt. rel.: ", barometro.getAltitudeRelativa(), "   Alt. pres.", barometro.getAltitudePressao())


        
            

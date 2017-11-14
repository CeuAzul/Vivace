"""FUNÇÃO GLOBAL
Código exemplo de utilização da biblioteca do Ultrassom (e escrita de arquivo com os dados)
"""
#!/usr/bin/python
import time
from lib.dado import Dado
from lib.ultrassomlib2 import Ultrassom
from lib.datilografo import Escritor

# Inicializa objetod do ultrassom e escritor
ultrassom = Ultrassom(30, 3, 23, 24)
escritor = Escritor(",", True, True, "Ultrassom - ", ".csv")

# Cria objeto dos dados
item = Dado("Item", "it", "itn", True, True, False)
tempo = Dado("Tempo", "Segundos", "tmp", True, True, False)
distanciaAtual = Dado("Distância Atual", "cm", "dsc", True, True, False)
distanciaReferencia = Dado("Distância de referência",
                           "cm", "dsr", True, True, False)
distanciaMaxima = Dado("Distância Maxima", "cm", "dsm", True, True, False)
elevacaoMinima = Dado("Elevação Mínima", "cm", "elm", True, True, False)
wowRaw = Dado("Wow primário", "bit", "wop", True, True, False)


inicio = int(round(time.time() * 1000))
ultrassom.inicializa()


def atualizaEscritor():
    """Atualiza vetor de dados e manda-os para o escritor
    """
    d = [tempo, item, distanciaAtual, distanciaReferencia,
         distanciaMaxima, elevacaoMinima, wowRaw]
    escritor.setDados(d)


def atualizaUltrassom():
    """Atualiza dados do ultrassom e passa para as variáveis do código global
    """
    ultrassom.atualiza()
    distanciaAtual.setValor(ultrassom.getDistanciaAtual())
    distanciaReferencia.setValor(ultrassom.getDistanciaReferencia())
    distanciaMaxima.setValor(ultrassom.getDistanciaMax())
    elevacaoMinima.setValor(ultrassom.getElevacaoMin())
    wowRaw.setValor(ultrassom.getWowRaw())


# Faz cabeçalho
atualizaEscritor()
escritor.fazCabecalho()


tempoAgora = int(round(time.time() * 1000)) - inicio
item.setValor(0)
print("calibrou")

# Cria loop de atualização e escrita no arquivo, cada iteração é uma linha e uma atualização
while tempoAgora <= 20000:
    atualizaUltrassom()
    item.setValor(item.getValor() + 1)
    tempoAgora = int(round(time.time() * 1000)) - inicio
    tempo.setValor(tempoAgora)
    atualizaEscritor()
    escritor.escreveLinhaDado()
    print(ultrassom.getDistanciaAtual())
    time.sleep(0.4)
ultrassom.finaliza()

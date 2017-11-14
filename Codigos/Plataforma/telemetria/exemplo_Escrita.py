"""FUNÇÃO GLOBAL
Código exemplo de utilização da biblioteca "Escritor"
"""
#!/usr/bin/python
from lib.dado import Dado
from lib.datilografo import Escritor

# Cria objeto Escritor
escritor = Escritor("\t", True, True, "Telemetria - ", ".csv")

# Cria alguns dados para serem utilizados como teste
tempo = Dado("Tempo", "Segundos", "tmp", True, True, True, 3)
rpm = Dado("Rotação do motor", "Rpm", "rpm", True, True, False, 4)
posicaoX = Dado("Posição X GPS", "Metros", "pox", True, False, False, 1)


def atualizaEscritor():
    """Atualiza vetor de dados e passa eles para o Escritor
    """
    d = [tempo, rpm, posicaoX]
    escritor.setDados(d)


# Faz cabeçalho
atualizaEscritor()
escritor.fazCabecalho()

# Faz iterações de escritas de linha, modificando os valore dos dados
for x in range(1000):
    tempo.setValor(1.25)
    rpm.setValor(1000 + x + 1.3)
    posicaoX.setValor(200 + x)
    atualizaEscritor()
    escritor.escreveLinhaDado()
    print(escritor.verificaTamanhoArquivo())

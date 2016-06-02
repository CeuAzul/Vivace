"""FUNÇÃO GLOBAL
Código exemplo de utilização da biblioteca "Escritor"
"""
#!/usr/bin/python
from lib.dado import Dado
from lib.datilografo import Escritor

#Cria objeto Escritor
escritor = Escritor("   ", True, True, "Telemetria - ", ".csv")

#Cria alguns dados para serem utilizados como teste
tempo = Dado("Tempo", "Segundos", "tmp", True, True, True)
rpm = Dado("Rotação do motor", "Rpm", "rpm", True, True, False)
posicaoX = Dado("Posição X GPS", "Metros", "pox", True, False, False)

def atualizaEscritor():
    """Atualiza vetor de dados e passa eles para o Escritor
    """
    d = [tempo, rpm, posicaoX]
    escritor.setDados(d)

#Faz cabeçalho
atualizaEscritor()
escritor.fazCabecalho()

#Faz iterações de escritas de linha, modificando os valore dos dados
for x in range(10):
    tempo.setValor(1+x)
    rpm.setValor(1000+x)
    posicaoX.setValor(200+x)
    atualizaEscritor()
    escritor.escreveLinhaDado()


        
            

"""FUNÇÃO GLOBAL
Código exemplo de utilização da biblioteca "pitot8b"
Referente a utilização do pitot com o ADC de 8bits
"""
#!/usr/bin/python
from lib.dado import Dado
from lib.datilografo import Escritor
from lib.pitot8b import Pitot8b
import time

#Cria objeto Escritor
escritor = Escritor("   ", True, True, "Pitot 8b - ", ".csv")

#Cria objeto do pitot com ADC 8 bits
pitot8b = Pitot8b(0);
pitot8b2 = Pitot8b(1);
pitot8b3 = Pitot8b(2);
pitot8b4 = Pitot8b(3);



#Cria alguns dados do pitot
item = Dado("Item", "it", "itn", True, True, False)
tempo = Dado("Tempo", "Segundos", "tmp", True, True, False)
valADC = Dado("Valor direto do ADC", "byte", "ppa", True, True, True)
tensao = Dado("Tensao", "V", "ppv", True, True, False)
pressaoDin = Dado("PressaoDinamica", "PA", "ppp", True, False, False)
velcas = Dado("Velocidade calibrada", "m/s", "vel", True, True, True)
velcas2 = Dado("Velocidade calibrada Pitot 2", "m/s", "vel2", True, True, True)
velcas3 = Dado("Velocidade calibrada Pitot 3", "m/s", "vel3", True, True, True)
velcas4 = Dado("Velocidade calibrada Pitot 4", "m/s", "vel4", True, True, True)
rpm1 = Dado("rpm1", "rpm", "rpm1", True, True, True)
rpm2 = Dado("rpm2", "rpm", "rpm2", True, True, True)

inicio = int(round(time.time()*1000))

def atualizaEscritor():
    """Atualiza vetor de dados e passa eles para o Escritor
    """
    d = [item, tempo, valADC, tensao, pressaoDin, velcas, velcas2, velcas3, velcas4, rpm1, rpm2]
    escritor.setDados(d)

#Faz cabeçalho
atualizaEscritor()
escritor.fazCabecalho()
tempoAgora = int(round(time.time()*1000)) - inicio
item.setValor(0)

#Faz iterações de escritas de linha, modificando os valore dos dados
for x in range(1000):
    pitot8b.atualiza(10, 1.218)
    pitot8b2.atualiza(20, 1.218)
    pitot8b3.atualiza(10, 1.218)
    pitot8b4.atualiza(10, 1.218)
    valADC.setValor(pitot8b.getValADC())
    tensao.setValor(pitot8b.getValTensao())
    pressaoDin.setValor(pitot8b.getPressaoDinamica())
    velcas.setValor(pitot8b.getVelocidade())
    velcas2.setValor(pitot8b2.getVelocidade())
    velcas3.setValor(pitot8b3.getVelocidade())
    velcas4.setValor(pitot8b4.getVelocidade())
    rpm1.setValor(pitot8b4.getRPM())
    rpm2.setValor(pitot8b3.getRPM())

    if(x == 250):
        pitot8b.setReferenciaAqui(20)

    if(x == 500):
        pitot8b.setReferenciaAqui(20)
        

    item.setValor(item.getValor()+1)
    tempoAgora = int(round(time.time()*1000)) - inicio
    tempo.setValor(tempoAgora)
    print(velcas.getValor(), velcas2.getValor(), rpm1.getValor(), rpm2.getValor())
    atualizaEscritor()
    escritor.escreveLinhaDado()


        #valADC.getValor(),", ", tensao.getValor(),", ", pressaoDin.getValor(),", ",
            

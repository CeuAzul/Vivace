"""Biblioteca Pitot
Biblioteca irá converter os dados do ADC para um valor de velocidade e pressão
"""
#!/usr/bin/python
import time
from .adc8 import ADC8
from random import randint

class Pitot8b:
    """Biblioteca Pitot
    Biblioteca irá converter os dados do ADC para um valor de velocidade e pressão
    Primeiramente será convertido o valor do ADC para um nível de tensão
    Depois, essa tensão é convertida em pressão
    E por fim, é convertida em velocidade
    """
    def __init__(self, numADC=0):
        #Cria objeto do ADC
        self.adc8 = ADC8()
        self.numADC = numADC
        self.valADC = 0
        self.valTensao = 0
        self.pressaoDinamica = 0
        self.velocidade = 0
        self.valorInicial = 58
        self.setReferenciaAqui()

    def setReferenciaAqui(self, samples=20):
        for x in range(samples):
            self.atualiza(10)
            self.valorInicial = self.valADC
            time.sleep(0.01)

    def atualiza(self, samples=20, densAr=1.218):
        """Le valor analogico do ADC e transforma isso em pressão e velocidade
        :param samples: Número de amostras para oversampling.
        """
        self.valADC = 0
        for x in range(samples):
 
            if self.numADC==0:
                self.valADC += self.adc8.getCanal0()
            elif self.numADC==1:
                self.valADC += self.adc8.getCanal2()
            elif self.numADC==2:
                self.valADC += self.adc8.getCanal1()
            elif self.numADC==3:
                self.valADC += self.adc8.getCanal3()
            else:
                self.valADC += self.adc8.getCanal0()

        self.valADC = self.valADC/samples
        
        #Sabemos que 255 equivale a 3.3 V
        self.valTensao = 3.3*(self.valADC-self.valorInicial)/255

        #Utilizamos a equação do datasheet para encontra a pressão em PA
        self.pressaoDinamica = ((self.valTensao)/0.66)*1000

        #Só ruído
        if self.pressaoDinamica < 0:
            self.pressaoDinamica = 0
    
        #Esquadrão anti-burrice
        if densAr <= 0:
            densAr = 1.218
            

        #E outra formulinha de mec flu
        self.velocidade = (abs(self.pressaoDinamica*2/densAr))**(1/2) 

    def getValADC(self):
        """Retorna o valor vindo direto do adc
            :returns: Valor do ADC
        """
        return self.valADC

    def getValTensao(self):
        """Retorna o valor da tensão do pitot
            :returns: Tensão (Volts)
        """
        return self.valTensao

    def getRPM(self):
        """Retorna um valor aproximado em RPM caso o pitot esteja no escoamento do motor
            :returns: RPM 
        """
        rpm = (640*self.velocidade-166.67)
        rpm = round(rpm, -1)

        if rpm < 0:
            rpm = 0
        if rpm > 24320:
            rpm = 24000-(randint(0,10))*100
            
        return rpm

    def getPressaoDinamica(self, um="m/s"):
        """Retorna valor da pressão dinâmica
            :returns: pressão dinâmica
            :param um: Unidade de medida.
        """
        if um=="PA":
            return self.pressaoDinamica
        elif um=="hPA":
            return self.pressaoDinamica/100
        elif um=="mBar":
            return self.pressaoDinamica/100
        else: #retorna PA
            return self.pressaoDinamica

    def getVelocidade(self, um="m/s"):
        """Retorna valor da velocidade calibrada
            :returns: Velocidade calibrada
            :param um: Unidade de medida.
        """
        if um == "m/s":
            return self.velocidade
        elif um == "km/h":
            return self.velocidade*3.6
        elif um == "nós":
            return self.velocidade*1.94384
        else:
            #velocidade em m/s
            return self.velocidade
            

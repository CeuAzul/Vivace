#!/usr/bin/python
# -*- coding: utf-8 -*-

class Pitot:
    """Classe responsavel pela criaçao e comunicaçao de objetos do tipo Pitot.
    Esta classe ira converter os dados analogicos vindos do ADC em dados de
    pressao e velocidade:

    1. Primeiramente será convertido o valor do ADC para um nível de tensão.
    2. Depois, essa tensão é convertida em pressão.
    3. E por fim, é convertida em velocidade.
    """

    def __init__(self, nome, apelido, cal_factor, arduino, UM = "V"):
        """Inicializa o objeto Pitot na porta analogica especificada.

        :param numADC: Numero da porta ADC a ser utilizada
        """
        self.nome =  nome
        self.apelido = apelido
        self.calibration_factor = cal_factor
        self.arduino = arduino
        self.UM = UM

        self.rawPitotData = 0
        self.pressaoDinamica = 0
        self.pressaoDinamicaRef = 0
        self.velocidade = 0
        self.velocidadeRef = 0
        self.refPitotData = 0
        self.refPressaoDin = 0
        self.ultimosCemRawPitotData = [0] * 100

    def atualiza(self, densAr=1.218):
        """Le valor analogico do ADC e transforma isso em pressão e
        velocidade. Todas as variaveis sao entao atualizadas.

        :param samples: Número de amostras para oversampling
        :param densAr: Densidade local do ar
        """

        dicioDeDados = self.arduino.dicioDeDados
        if self.apelido in dicioDeDados:
            self.rawPitotData = dicioDeDados[self.apelido]

        self.ultimosCemRawPitotData.pop(0)
        self.ultimosCemRawPitotData.append(self.rawPitotData)

        self.pressaoDinamica = self.rawPitotData * self.calibration_factor
        self.pressaoDinamicaRef = self.pressaoDinamica - self.refPressaoDin

        # Esquadrão anti-burrice
        if densAr <= 0:
            densAr = 1.218

        # E outra formulinha de mec flu
        self.velocidade = (abs(self.pressaoDinamica * 2 / densAr))**(1 / 2)
        self.velocidadeRef = (abs((self.pressaoDinamicaRef) * 2 / densAr))**(1 / 2)

    def setRefPitot(self, samples=100):
        """Seta um valor de referencia para as futuras aquisiçoes.
        Sera coletado um numero de samples analogicos especificado,
        uma media desses valores sera realizada e este valor medio
        sera utilizado futuramente como "zero" de referencia.

        :param: samples: Número de amostras para oversampling
        """
        self.refPitotData = sum(self.ultimosCemRawPitotData[-samples:]) / samples
        self.refPressaoDin = self.refPitotData * self.calibration_factor
        print("Zero do " + self.nome + ": " + str(self.refPitotData))


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

    def __init__(self, nome, apelido, arduino, UM = "V"):
        """Inicializa o objeto Pitot na porta analogica especificada.

        :param numADC: Numero da porta ADC a ser utilizada
        """
        self.nome =  nome
        self.apelido = apelido
        self.arduino = arduino
        self.UM = UM

        self.pressaoDinamica = 0
        self.velocidade = 0
        self.refPressaoDin = 0
        self.refPressaoDin = 0
        self.ultimosCemPressaoDin = [0] * 100

    def atualiza(self, densAr=1.218):
        """Le valor analogico do ADC e transforma isso em pressão e
        velocidade. Todas as variaveis sao entao atualizadas.

        :param samples: Número de amostras para oversampling
        :param densAr: Densidade local do ar
        """

        dicioDeDados = self.arduino.getData()
        if self.apelido in dicioDeDados:
            self.pressaoDinamica = dicioDeDados[self.apelido]

        self.ultimosCemPressaoDin.pop(0)
        self.ultimosCemPressaoDin.append(self.pressaoDinamica)

        # Esquadrão anti-burrice
        if densAr <= 0:
            densAr = 1.218

        # E outra formulinha de mec flu
        self.velocidade = (abs(self.pressaoDinamica * 2 / densAr))**(1 / 2)

    def setRefPressaoDin(self, samples=100):
        """Seta um valor de referencia para as futuras aquisiçoes.
        Sera coletado um numero de samples analogicos especificado,
        uma media desses valores sera realizada e este valor medio
        sera utilizado futuramente como "zero" de referencia.

        :param: samples: Número de amostras para oversampling
        """
        self.refPressaoDin = sum(self.ultimosCemPressaoDin[-samples:]) / samples
        print("Zero do " + self.nome + ": " + str(self.refPressaoDin))

    def getPressaoDin(self, um="Pa"):
        """Retorna valor da pressão dinâmica.

            :param um: Unidade de medida
            :returns: pressão dinâmica
        """
        if um == "Pa":
            return self.pressaoDinamica
        elif um == "hPa":
            return self.pressaoDinamica / 100
        elif um == "mBar":
            return self.pressaoDinamica / 100
        else:  # retorna Pa
            return self.pressaoDinamica

    def getVelocidade(self, um="m/s"):
        """Retorna valor da velocidade calibrada.

            :param um: Unidade de medida
            :returns: Velocidade calibrada
        """
        if um == "m/s":
            return self.velocidade
        elif um == "km/h":
            return self.velocidade * 3.6
        elif um == "nós":
            return self.velocidade * 1.94384
        else:
            # velocidade em m/s
            return self.velocidade

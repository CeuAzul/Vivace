#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
if os.uname()[1] == 'raspberrypi':
    import RPi.GPIO as GPIO
import time
import datetime


class Ultrassom:
    """Classe do sensor de ultrassom, responsavel por avaliar se o aviao
    ja decolou ou se ainda se encontra em solo.
    """

    def __init__(self, distMax=30, elevacaoMin=3, trigPin=23, echoPin=24):
        """Inicializa o objeto ultrassom com os parametros especificados.

        :param distMax: Distancia de pista percorrida (?)
        :param elevacaoMin: Elevaçao minima para que se considere uma decolagem
        :param trigPin: Porta do pino de Trig do ultrassom
        :param echoPin: Porta do pino de Echo do ultrassom
        """

        GPIO.setmode(GPIO.BCM)
        self.trigPin = trigPin
        self.echoPin = echoPin
        self.distMax = distMax
        self.distAtual = 0
        self.distReferencia = 0
        self.wowRaw = 0
        self.elevacaoMin = elevacaoMin

    def calculaDistancia(self):
        """Calcula a distancia entre o ultrassom e o objeto que esta
        "tapando" ele, idealmente o chao.

        :returns: Distancia do ultrassom ao chao.
        """

        distance = 0
        cont = 0
        while(distance <= 0 or distance >= self.distMax):
            time.sleep(0.5)
            GPIO.output(self.trigPin, True)
            time.sleep(0.00001)
            GPIO.output(self.trigPin, False)

            tempoInicio = time.time()
            pulse_start = time.time()
            while GPIO.input(self.echoPin) == 0:
                pulse_start = time.time()
                duracao = pulse_start - tempoInicio
                if duracao > (self.distMax / 17150):
                    return self.distMax

            pulse_end = time.time()
            while GPIO.input(self.echoPin) == 1:
                pulse_end = time.time()
                duracao = pulse_end - tempoInicio
                if duracao > (self.distMax / 17150):
                    return self.distMax

            pulse_duration = pulse_end - pulse_start
            distance = pulse_duration * 17150
            distance = round(distance, 2)
            cont = cont + 1
            if(cont > 5):
                return self.distMax
        return distance

    def calibraAqui(self, calibracoes=20):
        """Zera a altura do ultrassom de modo a se ter uma referencia da
        altura em que ele foi instalado com relaçao ao solo.
        """

        dist = 0
        for i in range(calibracoes):
            dist = dist + self.calculaDistancia()
        dist = dist / calibracoes
        self.distReferencia = round(dist, 2)

    def inicializa(self):
        """Inicializa as portas GPIO de Trig como output e Echo como input,
        coloca a porta trig como baixa e calibra a altura de ultrassom.
        """

        GPIO.setup(self.trigPin, GPIO.OUT)
        GPIO.setup(self.echoPin, GPIO.IN)
        GPIO.output(self.trigPin, False)
        time.sleep(2)
        self.calibraAqui()

    def atualiza(self):
        """Atualiza as variaveis de distancia atual e a booleana wowRaw.
        """
        self.distAtual = self.calculaDistancia()
        # 0 = no solo
        # 1 = Voando
        if(self.distAtual > (self.distReferencia + self.elevacaoMin)):
            self.wowRaw = 1
        else:
            self.wowRaw = 0

    def finaliza(self):
        """Limpa as portas GPIO
        """
        GPIO.cleanup()

    def getDistanciaAtual(self):
        """Retorna o valor de distancia percorrida em pista.

        :returns: Distancia percorrida em pista
        """
        return self.distAtual

    def getWowRaw(self):
        """Retorna o valor de WeightOnWhells cru.

        :returns: WeightOnWhells cru
        """
        return self.wowRaw

    def getDistanciaReferencia(self):
        """Retorna o valor da distancia usada como referencia.

        :returns: Distancia de referencia
        """
        return self.distReferencia

    def getDistanciaMax(self):
        """Retorna o valor da distancia final de pista percorrida.

        :returns: Distancia de pista percorrida
        """
        return self.distMax

    def getElevacaoMin(self):
        """Retorna o valor da elevaçao minima para ser considerada decolagem.

        :returns: Elevaçao minima de decolagem
        """
        return self.elevacaoMin

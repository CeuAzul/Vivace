import RPi.GPIO as GPIO
import time
import datetime


class Ultrassom:

    def __init__(self, distMax=30, elevacaoMin=3, trigPin=23, echoPin=24):
        GPIO.setmode(GPIO.BCM)
        self.trigPin = trigPin
        self.echoPin = echoPin
        self.distMax = distMax
        self.distAtual = 0
        self.distReferencia = 0
        self.wowRaw = 0
        self.elevacaoMin = elevacaoMin

    def calculaDistancia(self):
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
        dist = 0
        for i in range(calibracoes):
            dist = dist + self.calculaDistancia()
        dist = dist / calibracoes
        self.distReferencia = round(dist, 2)

    def inicializa(self):
        GPIO.setup(self.trigPin, GPIO.OUT)
        GPIO.setup(self.echoPin, GPIO.IN)
        GPIO.output(self.trigPin, False)
        time.sleep(2)
        self.calibraAqui()

    def atualiza(self):
        self.distAtual = self.calculaDistancia()
        # 0 = no solo
        # 1 = Voando
        if(self.distAtual > (self.distReferencia + self.elevacaoMin)):
            self.wowRaw = 1
        else:
            self.wowRaw = 0

    def finaliza(self):
        GPIO.cleanup()

    def getDistanciaAtual(self):
        return self.distAtual

    def getWowRaw(self):
        return self.wowRaw

    def getDistanciaReferencia(self):
        return self.distReferencia

    def getDistanciaMax(self):
        return self.distMax

    def getElevacaoMin(self):
        return self.elevacaoMin

import RPi.GPIO as GPIO
import time
import datetime

class Ultrassom:

  def __init__(self, distMax=30, elevacaoMin=3, trigPin=23, echoPin=24):
    GPIO.setmode(GPIO.BCM)
    self.trigPin = trigPin 
    self.echoPin = echoPin
    #set GPIO direction (IN / OUT)
    GPIO.setup(self.trigPin, GPIO.OUT)
    GPIO.setup(self.echoPin, GPIO.IN)
    self.distMax = distMax
    self.distAtual = 0
    self.distReferencia = 0
    self.wowRaw = 0
    self.elevacaoMin = elevacaoMin



  def calculaDistancia(self):
    distance = 0
    cont = 0
    while(distance<=0 or distance>=self.distMax):
      # set Trigger to HIGH
      GPIO.output(self.trigPin, True)
   
      # set Trigger after 0.01ms to LOW
      time.sleep(0.00001)
      GPIO.output(self.trigPin, False)
   
      StartTime = time.time()
      StopTime = time.time()
   
      # save StartTime
      while GPIO.input(self.echoPin) == 0:
          StartTime = time.time()
   
      # save time of arrival
      while GPIO.input(self.echoPin) == 1:
          StopTime = time.time()
   
      # time difference between start and arrival
      TimeElapsed = StopTime - StartTime
      # multiply with the sonic speed (34300 cm/s)
      # and divide by 2, because there and back
      distance = (TimeElapsed * 34300) / 2
   

      distance = round(distance, 2)
      cont = cont+1
      if(cont > 5):
        return self.distMax
    return distance

  def calibraAqui(self, calibracoes=20):
    dist = 0
    for i in range(calibracoes):
      dist = dist + self.calculaDistancia()
    dist = dist/calibracoes
    self.distReferencia = round(dist, 2)



  def inicializa(self):
    GPIO.setup(self.trigPin,GPIO.OUT)
    GPIO.setup(self.echoPin,GPIO.IN)
    GPIO.output(self.trigPin, False)
    time.sleep(2)
    self.calibraAqui()
    

  def atualiza(self):
    self.distAtual = self.calculaDistancia()
    ## 0 = no solo
    ## 1 = Voando
    if(self.distAtual > (self.distReferencia+self.elevacaoMin)):
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

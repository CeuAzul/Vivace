import RPi.GPIO as GPIO
import time
import datetime

GPIO.setmode(GPIO.BCM)

TRIG = 23 
ECHO = 24

print("Distance Measurement In Progress")

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

GPIO.output(TRIG, False)
print("Waiting For Sensor To Settle")
time.sleep(0.5)
inicio = int(round(time.time()*1000))
tempoAgora = int(round(time.time()*1000)) - inicio
while tempoAgora <= 20000 :
  tempoAgora = int(round(time.time()*1000)) - inicio
  tempoAntesFuncao = datetime.datetime.now()
  GPIO.output(TRIG, True)
  time.sleep(0.00001)
  GPIO.output(TRIG, False)

  while GPIO.input(ECHO)==0:
    pulse_start = time.time()

  while GPIO.input(ECHO)==1:
    pulse_end = time.time()

  pulse_duration = pulse_end - pulse_start

  distance = pulse_duration * 17150

  distance = round(distance, 2)

  tempoDepoisFuncao = datetime.datetime.now()
  tempoFuncao = tempoDepoisFuncao - tempoAntesFuncao
  print("Distance: ",distance,"cm")
  print("Tempo: ", tempoFuncao.microseconds)
  time.sleep(0.1)
GPIO.cleanup()

import os
import time

temTransmit = os.path.exists('/dev/ttyUSB0')
temNano = os.path.exists('/dev/ttyUSB1')

while(not temTransmit):
    temTransmit = os.path.exists('/dev/ttyUSB0')
    print("Transmissor não detectado")

while(not temNano):
    temNano = os.path.exists('/dev/ttyUSB1')
    print("Nano não detectado")

if (temTransmit):
    if(temNano):
        time.sleep(3)
        os.system(
            "/usr/bin/python3 /home/pi/Telemetria/Codigos/Plataforma/telemetria/codigo-global_servo.py")

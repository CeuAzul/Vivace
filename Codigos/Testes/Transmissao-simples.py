import serial
import time
ser = serial.Serial('/dev/ttyUSB0', 57600)

while True:
    print("Transmitindo")
    ser.write(bytes('Um pequeno bit no receptor é um grande salto na Telemetria!\n', 'UTF-8'))
    print("Transmitiu!")
    time.sleep(1)

#!/usr/bin/env python

import time
import serial

ser = serial.Serial(

    port='/dev/ttyUSB0',
    baudrate = 57600,
    timeout=1

    )

while 1:
    x=ser.readline().decode("utf-8")
    if(x != ""):
        print(x)

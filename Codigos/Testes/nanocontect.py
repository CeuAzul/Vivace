import serial

ser = serial.Serial(

    port='/dev/ttyUSB0',
    baudrate = 9600,
    timeout=1

    )
while 1:
    x=ser.readline().decode("utf-8")
    print(x)
    if(x != ""):
        print(x)
        x = x.replace("\r\n","")
        print(x)
        x = x.replace(" ","")
        print(x)
        y = x.split(";")
        print(y)

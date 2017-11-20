#!/usr/bin/python
# -*- coding: utf-8 -*-

import serial


class Nano:
    """ Pega dados do nano - Tacometro e Ultrassom
    """

    def __init__(self):
        """Construtor
        Bota os métodos para funcionar
        """

        self.ser = serial.Serial(port='/dev/ttyUSB1', baudrate=9600, timeout=1)

        self.wow = 0
        self.rpmD = 0
        self.rpmE = 0
        self.wowRaw = 0
        self.tempoVoo = 0
        self.distancia = 0
        self.distRef = 0

    def atualiza(self):
        """Atualiza a parada

        """
        x = self.ser.readline().decode("utf-8")
        if(x != ""):
            x = x.replace("\r\n", "")
            x = x.replace(" ", "")
            y = x.split(",")
            if len(y) == 7:
                self.wow = y[0]
                self.rpmD = y[1]
                self.rpmE = y[2]
                self.wowRaw = y[3]
                self.tempoVoo = y[4]
                self.distancia = y[5]
                self.distRef = y[6]

    def getWow(self):
        return self.wow

    def getRpmD(self):
        return self.rpmD

    def getRpmE(self):
        return self.rpmE

    def getWowRaw(self):
        return self.wowRaw

    def getTempoVoo(self):
        return self.tempoVoo

    def getDistancia(self):
        return self.distancia

    def getDistRef(self):
        return self.distRef

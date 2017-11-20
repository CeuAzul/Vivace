#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
if os.uname()[1] == 'raspberrypi':
    import smbus
import time


class ADC8:
    """Classe utilizada para realização da interface do ADC 8 bits
    com o restante da telemetria

    O ADC utilizado é o Waveshare PCF8591 ligado no I2C endereço 48
    """

    def __init__(self):
        """Construtor apenas cria o bus e seta o endereço i2c
        """
        self.bus = smbus.SMBus(1)
        self.address = 0x48

    def read(self, chn):
        """Le o canal pedido pela função
        :param chn: Canal do ADC que gostaria de ler (0 até 3)
        :returns: Valor analógico do canal especificado
        """
        if chn == 0:
            self.bus.write_byte(self.address, 0x40)
        if chn == 1:
            self.bus.write_byte(self.address, 0x41)
        if chn == 2:
            self.bus.write_byte(self.address, 0x42)
        if chn == 3:
            self.bus.write_byte(self.address, 0x43)
        self.bus.read_byte(self.address)  # dummy read to start conversion
        return self.bus.read_byte(self.address)

    def getCanal0(self):
        """Pega valor do canal 0
        :returns: Valor analógico do canal 0
        """
        return self.read(0)

    def getCanal1(self):
        """Pega valor do canal 1
        :returns: Valor analógico do canal 1
        """
        return self.read(1)

    def getCanal2(self):
        """Pega valor do canal 2
        :returns: Valor analógico do canal 2
        """
        return self.read(2)

    def getCanal3(self):
        """Pega valor do canal 3
        :returns: Valor analógico do canal 3
        """
        return self.read(3)

#!/usr/bin/python
# -*- coding: utf-8 -*-

import time

import os
if os.uname()[1] == 'raspberrypi':
    from smbus import SMBus


class Barometro:
    """Um objeto dessa classe deve ser criado quando quiser realizar a comunicação
    ou obter dados do barômetro.

    Para utilizar a classe, criamos o construtor colocando como parâmetros
    se queremos pegar temperatura e pressão. Depois, utilizamos a função
    atualiza() para fazer a aquisição pelo I2C. Por fim, pegamos os dados
    usando os getters().
    """
    __MS5611_ADDRESS_CSB_LOW = 0x76
    __MS5611_ADDRESS_CSB_HIGH = 0x77
    __MS5611_DEFAULT_ADDRESS = 0x77

    __MS5611_RA_ADC = 0x00
    __MS5611_RA_RESET = 0x1E

    __MS5611_RA_C0 = 0xA0
    __MS5611_RA_C1 = 0xA2
    __MS5611_RA_C2 = 0xA4
    __MS5611_RA_C3 = 0xA6
    __MS5611_RA_C4 = 0xA8
    __MS5611_RA_C5 = 0xAA
    __MS5611_RA_C6 = 0xAC
    __MS5611_RA_C7 = 0xAE

    __MS5611_RA_D1_OSR_256 = 0x40
    __MS5611_RA_D1_OSR_512 = 0x42
    __MS5611_RA_D1_OSR_1024 = 0x44
    __MS5611_RA_D1_OSR_2048 = 0x46
    __MS5611_RA_D1_OSR_4096 = 0x48

    __MS5611_RA_D2_OSR_256 = 0x50
    __MS5611_RA_D2_OSR_512 = 0x52
    __MS5611_RA_D2_OSR_1024 = 0x54
    __MS5611_RA_D2_OSR_2048 = 0x56
    __MS5611_RA_D2_OSR_4096 = 0x58

    def __init__(self, usePressao=True, useTemp=True):
        """Construtor: Indica dados a serem lidos

         Coloca parâmetros indicando se gostaria de utilizar o
         dado de pressão e/ou utilizar os dados de temperatura.
         Além disso a função configura os dados
         para que a comunicação I2C seja feita corretamente.

        :param usePressao: Indicador se deve ser obtido o dado de pressão
        :param useTemp: Indicador se deve ser obtido o dado de temperatura
        """
        self.bus = SMBus(1)
        self.address = 0x77
        self.C1 = 0
        self.C2 = 0
        self.C3 = 0
        self.C4 = 0
        self.C5 = 0
        self.C6 = 0
        self.D1 = 0
        self.D2 = 0

        self.temp = 0.0  # Calculated temperature
        self.pres = 0.0  # Calculated Pressure
        self.densidadeAr = 0
        self.altitudePressao = 0
        self.altitudeRelativa = 0

        self.pressaoReferencia = 0
        self.pressaoAtmosfericaPadrao = 101325

        self.usePressao = usePressao
        self.useTemp = useTemp

        # The MS6511 Sensor stores 6 values in the EPROM memory that we need in order to calculate the actual temperature and pressure
        # These values are calculated/stored at the factory when the sensor is calibrated.
        # I probably could have used the read word function instead of the whole block, but I wanted to keep things consistent.
        C1 = self.bus.read_i2c_block_data(
            self.address, self.__MS5611_RA_C1)  # Pressure Sensitivity
        # time.sleep(0.05)
        C2 = self.bus.read_i2c_block_data(
            self.address, self.__MS5611_RA_C2)  # Pressure Offset
        # time.sleep(0.05)
        # Temperature coefficient of pressure sensitivity
        C3 = self.bus.read_i2c_block_data(self.address, self.__MS5611_RA_C3)
        # time.sleep(0.05)
        # Temperature coefficient of pressure offset
        C4 = self.bus.read_i2c_block_data(self.address, self.__MS5611_RA_C4)
        # time.sleep(0.05)
        C5 = self.bus.read_i2c_block_data(
            self.address, self.__MS5611_RA_C5)  # Reference temperature
        # time.sleep(0.05)
        # Temperature coefficient of the temperature
        C6 = self.bus.read_i2c_block_data(self.address, self.__MS5611_RA_C6)

        # Again here we are converting the 2 8bit packages into a single decimal
        self.C1 = C1[0] * 256.0 + C1[1]
        self.C2 = C2[0] * 256.0 + C2[1]
        self.C3 = C3[0] * 256.0 + C3[1]
        self.C4 = C4[0] * 256.0 + C4[1]
        self.C5 = C5[0] * 256.0 + C5[1]
        self.C6 = C6[0] * 256.0 + C6[1]

        self.atualizaReferencia()

    def atualizaReferencia(self):
        self.pressaoReferencia = 0
        for i in range(0, 10):
            self.atualiza()
            self.pressaoReferencia = self.pressaoReferencia + self.getPressao()
        self.pressaoReferencia = self.pressaoReferencia / 10

    def refreshPressure(self, OSR=__MS5611_RA_D1_OSR_4096):
        """Função utilizada internamente para comunicação I2C.
        """
        self.bus.write_byte(self.address, OSR)

    def refreshTemperature(self, OSR=__MS5611_RA_D2_OSR_4096):
        """Função utilizada internamente para comunicação I2C.
        """
        self.bus.write_byte(self.address, OSR)

    def readPressure(self):
        """Função utilizada internamente para comunicação I2C.
        """
        D1 = self.bus.read_i2c_block_data(self.address, self.__MS5611_RA_ADC)
        self.D1 = D1[0] * 65536 + D1[1] * 256.0 + D1[2]

    def readTemperature(self):
        """Função utilizada internamente para comunicação I2C.
        """
        D2 = self.bus.read_i2c_block_data(self.address, self.__MS5611_RA_ADC)
        self.D2 = D2[0] * 65536 + D2[1] * 256.0 + D2[2]

    def calculatePressureAndTemperature(self):
        """Função utilizada internamente para comunicação I2C.

        É a função principal para realizar a aquisição dos dados via I2C.
        """
        dT = self.D2 - self.C5 * 2**8
        self.temp = 2000 + dT * self.C6 / 2**23

        OFF = self.C2 * 2**16 + (self.C4 * dT) / 2**7
        SENS = self.C1 * 2**15 + (self.C3 * dT) / 2**8

        if (self.temp >= 2000):
            T2 = 0
            OFF2 = 0
            SENS2 = 0
        elif (self.temp < 2000):
            T2 = dT * dT / 2**31
            OFF2 = 5 * ((self.temp - 2000) ** 2) / 2
            SENS2 = OFF2 / 2
        elif (self.temp < -1500):
            OFF2 = OFF2 + 7 * ((self.temp + 1500) ** 2)
            SENS2 = SENS2 + 11 * (self.temp + 1500) ** 2 / 2

        self.temp = self.temp - T2
        OFF = OFF - OFF2
        SENS = SENS - SENS2

        self.pres = (self.D1 * SENS / 2**21 - OFF) / 2**15

        self.temp = self.temp / 100  # Temperature updated
        self.pres = self.pres / 100  # Pressure updated

    def getPressao(self, um="PA"):
        """Retorna valor da pressão atual.

        :returns: Pressão atual
        :param um: Unidade de medida
        """
        if um == "PA":
            return self.pres * 100
        elif um == "hPA":
            return self.pres
        elif um == "mBar":
            return self.pres
        else:
            return self.pres

    def getTemperatura(self):
        """Retorna valor de temperatura.

        :returns: Temperatura (ºC)
        """
        return self.temp

    def getDensidadeAr(self):
        """Retorna Densidade do ar.

        :returns: Densidade
        """
        return self.densidadeAr

    def getAltitudeRelativa(self, um="m"):
        """Retorna altitude em relação ao lugar de calibração (solo).

        :param um: Unidade de medida
        :returns: Altitude em relação ao solo
        """
        if um == "m":
            return self.altitudeRelativa
        elif um == "ft":
            return self.altitudeRelativa * 3.28084
        else:  # retorna metros
            return self.altitudeRelativa

    def getAltitudePressao(self, um="m"):
        """Retorna a altitude-pressão.

        Altitude pressão é o valor da
        pressão de atmosfera padrão 101325 pascal.

        :param um: Unidade de medida
        :returns: Altitude-pressão em relação a atmosfera padrão
        """
        if um == "m":
            return self.altitudePressao
        elif um == "ft":
            return self.altitudePressao * 3.28084
        else:  # retorna metros
            return self.altitudePressao

    def atualiza(self, samples=1):
        """Retorna mais uma amostra dos parâmetros relacionados ao
        barômetro e armazena-os nas variáveis da classe.

        :param samples: Numero de samples adquiridos
        """
        somaTemp = 0
        somaPressao = 0
        for x in range(samples):
            if self.usePressao:
                self.refreshPressure()
                time.sleep(0.01)  # Waiting for pressure data ready
                self.readPressure()

            if self.useTemp:
                self.refreshTemperature()
                time.sleep(0.01)  # Waiting for temperature data ready
                self.readTemperature()

            self.calculatePressureAndTemperature()
            somaTemp = somaTemp + self.temp
            somaPressao = somaPressao + self.pres
        self.temp = somaTemp / samples
        self.pres = somaPressao / samples
        if self.useTemp:
            if self.usePressao:
                self.densidadeAr = self.pres * 100 / \
                    (287.05 * (self.temp + 273.15))
        if self.usePressao:
            if (self.pressaoReferencia != 0):
                self.altitudeRelativa = (
                    44330.0 * (1.0 - pow(self.pres * 100 / (self.pressaoReferencia), 0.1902949)))
            self.altitudePressao = (
                44330.0 * (1.0 - pow(self.pres * 100 / self.pressaoAtmosfericaPadrao, 0.1902949)))

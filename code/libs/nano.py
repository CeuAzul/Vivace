#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
if os.uname()[1] == 'raspberrypi':
    import serial


class Nano:
    """ Responsavel pela comunicaçao do RaspberryPi com um Arduino Nano
    conectado via porta USB e se comunicando através de protocolo Serial.abs

    Para utilizar esta classe basta que se crie um objeto da classe, sem
    parametros extras.

    Estao implementados nesta classe o retorno de variaveis relacionadas
    ao sensor de ultrassom e o tacometro.
    """

    def __init__(self):
        """Construtor: Inicializa o objeto da classe e inicializa a
        comunicaçao serial via porta USB1, com baudrate igual a 9600bps.
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
        """Atualiza todas as variaveis setadas dentro da classe.
        Atualmente as variaveis usadas sao:

        - wow
        - rpmD
        - rpmE
        - wowRaw
        - tempoVoo
        - distancia
        - distRef
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
        """ Retorna o valor de WeightOnWhells.

        :returns: WeightOnWhells
        """
        return self.wow

    def getRpmD(self):
        """ Retorna o valor de RPM no motor direito.

        :returns: RPM no motor direito
        """
        return self.rpmD

    def getRpmE(self):
        """ Retorna o valor de RPM no motor esquerdo.

        :returns: RPM no motor esquerdo
        """
        return self.rpmE

    def getWowRaw(self):
        """ Retorna o valor de WeightOnWhells cru.

        :returns: WeightOnWhells cru
        """
        return self.wowRaw

    def getTempoVoo(self):
        """ Retorna o valor de tempo atual de voo.

        :returns: Tempo atual de voo
        """
        return self.tempoVoo

    def getDistancia(self):
        """ Retorna o valor de distancia percorrida em pista.

        :returns: Distancia percorrida em pista
        """
        return self.distancia

    def getDistRef(self):
        """ Retorna o valor da distancia usada como referencia.

        :returns: Distancia de referencia
        """
        return self.distRef

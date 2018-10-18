#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import serial
import serial.tools.list_ports as prtlst


class Arduino:
    """ Responsavel pela comunicaçao do RaspberryPi com um Arduino Nano
    conectado via porta USB e se comunicando através de protocolo Serial.abs

    Para utilizar esta classe basta que se crie um objeto da classe, sem
    parametros extras.

    Estao implementados nesta classe o retorno de variaveis relacionadas
    ao sensor de ultrassom e o tacometro.
    """

    def __init__(self, baudrate=115200):
        """Construtor: Inicializa o objeto da classe e inicializa a
        comunicaçao serial via porta USB1, com baudrate igual a 9600bps.
        """

        self.codificacao = "utf-8"
        self.baudrate = baudrate
        self.dicioDeDados = dict()
        self.connect()

    def connect(self):
        print("########## Trying Arduino! ##########")
        pts = prtlst.comports()
        for pt in pts:
            if 'USB' or 'ACM' in pt[0]:
                if 'USB2.0' in pt[1]:
                    self.porta = pt[0]
                    self.devName = pt[1]
                    print('Connecting on Arduino ' + self.devName + ' on port ' + self.porta)
                    self.serial = serial.Serial(port=self.porta, baudrate=self.baudrate, timeout=1)

    def updateData(self):
        """Puxa linha de dados pela porta serial (Arduino).
        Puxa uma linha de dados começando com "!" e terminando em "@",
        separa os dados por ";" e separa cada dado entre "apelido" e "valor".
        Por fim, retorna um dicionario com apelidos e valores.
        """

        try:
            linha_de_dados = self.serial.readline().decode(self.codificacao)

            if(linha_de_dados != ""):
                linha_de_dados = linha_de_dados.replace("\r\n", "")
                if linha_de_dados.startswith("!") and linha_de_dados.endswith("@"):
                    linha_de_dados = linha_de_dados.replace(" ", "")
                    linha_de_dados = linha_de_dados.replace("!", "")
                    linha_de_dados = linha_de_dados.replace("@", "")
                    dados = linha_de_dados.split(";")
                    receivedChecksum = 0
                    calculatedChecksum = 0
                    tempDicioDeDados = {}
                    for dado in dados:
                        try:
                            apelido, valor = dado.split("=")
                            if apelido != 'cks':
                                calculatedChecksum += float(valor)
                                tempDicioDeDados[apelido] = float(valor)
                            else:
                                receivedChecksum = valor
                        except:
                            pass
                    if float(receivedChecksum) == float(calculatedChecksum):
                        self.dicioDeDados.update(tempDicioDeDados)
        except:
            pass

    def sendCommand(self, comando):

        try:
            self.serial.write(bytes("!" + comando + "@\n", self.codificacao))
        except:
            pass

    def getData(self):
        return self.dicioDeDados

#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
if os.uname()[1] == 'raspberrypi':
    import serial

import serial


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
        self.linha_de_dados = ""

        print("########## Trying Arduino on port ttyUSB0! ##########")
        try:
            self.ser = serial.Serial(port='/dev/ttyUSB0', baudrate=self.baudrate, timeout=1)
            print("########## Arduino connected! ##########")
        except:
            print("########## Trying Arduino on port ttyUSB1! ##########")
            try:
                self.ser = serial.Serial(port='/dev/ttyUSB1', baudrate=self.baudrate, timeout=1)
                print("########## Arduino connected! ##########")
            except:
                print("########## Trying Arduino on port ttyUSB2! ##########")
                try:
                    self.ser = serial.Serial(port='/dev/ttyUSB2', baudrate=self.baudrate, timeout=1)
                    print("########## Arduino connected! ##########")
                except:
                    print("########## Trying Arduino on port ttyACM0! ##########")
                    try:
                        self.ser = serial.Serial(port='/dev/ttyACM0', baudrate=self.baudrate, timeout=1)
                        print("########## Arduino connected! ##########")
                    except:
                        sys.exit("########## Arduino not detected! ##########")

    def getData(self):
        """Puxa linha de dados pela porta serial (Arduino).
        Puxa uma linha de dados começando com "!" e terminando em "@",
        separa os dados por ";" e separa cada dado entre "apelido" e "valor".
        Por fim, retorna um dicionario com apelidos e valores.
        """

        dict = {}

        try:
            self.linha_de_dados = self.ser.readline().decode(self.codificacao)
        except:
            pass

        if(self.linha_de_dados != ""):
            self.linha_de_dados = self.linha_de_dados.replace("\r\n", "")
            if self.linha_de_dados.startswith("!") and self.linha_de_dados.endswith("@"):
                self.linha_de_dados = self.linha_de_dados.replace(" ", "")
                self.linha_de_dados = self.linha_de_dados.replace("!", "")
                self.linha_de_dados = self.linha_de_dados.replace("@", "")
                dados = self.linha_de_dados.split(";")
                for dado in dados:
                    try:
                        apelido, valor = dado.split("=")
                        dict[apelido] = float(valor)
                    except:
                        pass

        return dict

    def sendCommand(self, comando):

        self.ser.write(bytes("!" + comando + "@\n", self.codificacao))

#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
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

    def __init__(self, porta='/dev/ttyUSB0', baudrate=115200):
        """Construtor: Inicializa o objeto da classe e inicializa a
        comunicaçao serial via porta USB1, com baudrate igual a 9600bps.
        """

        self.codificacao = "utf-8"
        self.baudrate = baudrate
        self.porta = porta
        self.dicioDeDados = dict()
        self.connect()

    def connect(self):
        print("########## Trying Arduino on port " + self.porta + "! ##########")
        self.ser = serial.Serial(port=self.porta, baudrate=self.baudrate, timeout=1)

    def updateData(self):
        """Puxa linha de dados pela porta serial (Arduino).
        Puxa uma linha de dados começando com "!" e terminando em "@",
        separa os dados por ";" e separa cada dado entre "apelido" e "valor".
        Por fim, retorna um dicionario com apelidos e valores.
        """

        try:
            linha_de_dados = self.ser.readline().decode(self.codificacao)

            if(linha_de_dados != ""):
                linha_de_dados = linha_de_dados.replace("\r\n", "")
                if linha_de_dados.startswith("!") and linha_de_dados.endswith("@"):
                    linha_de_dados = linha_de_dados.replace(" ", "")
                    linha_de_dados = linha_de_dados.replace("!", "")
                    linha_de_dados = linha_de_dados.replace("@", "")
                    dados = linha_de_dados.split(";")
                    for dado in dados:
                        try:
                            apelido, valor = dado.split("=")
                            self.dicioDeDados[apelido] = float(valor)
                        except:
                            pass
        except:
            pass

    def sendCommand(self, comando):

        try:
            self.ser.write(bytes("!" + comando + "@\n", self.codificacao))
        except:
            pass

    def getData(self):
        return self.dicioDeDados

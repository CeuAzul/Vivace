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

    def __init__(self):
        """Construtor: Inicializa o objeto da classe e inicializa a
        comunicaçao serial via porta USB1, com baudrate igual a 9600bps.
        """

        try:
            self.ser = serial.Serial(port='/dev/ttyUSB2', baudrate=115200, timeout=1)
            print("########## Arduino connected! ##########")
        except:
            sys.exit("########## Arduino not detected! ##########")

        self.codificacao = "utf-8"
        self.linha_de_dados = ""

    def getData(self):
        """Puxa linha de dados pela porta serial (Arduino).
        Puxa uma linha de dados começando com "!" e terminando em "@",
        separa os dados por ";" e separa cada dado entre "apelido" e "valor".
        Por fim, retorna um dicionario com apelidos e valores.
        """

        dict = {}

        if(linha_de_dados != ""):
            linha_de_dados = linha_de_dados.replace("\r\n", "")
            linha_de_dados = linha_de_dados.replace(" ", "")
            dados = linha_de_dados.split(";")
            for dado in dados:
                apelido, valor = dado.split("=")
                dict[apelido] = valor
        try:
            self.linha_de_dados = self.ser.readline().decode(self.codificacao)
        except:
            pass

        return dict

    def sendCommand(self, comando):

        self.ser.write(bytes("!" + comando + "@\n", self.codificacao))

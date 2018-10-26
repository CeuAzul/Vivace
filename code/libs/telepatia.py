#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import serial
import serial.tools.list_ports as prtlst
from .dado import Dado


class Transmissor:
    """ Esta classe é chamada toda vez que queremos transmitir um dado usando o transceiver da 3DR.
    Depois de criar os dados, utiza-se a função setDados() para popular o vetor dessa classe com os
    dados a serem transmitidos.

    Para utilizar a classe:

    - Primeiramente utilize o construtor para setar propriedades.
    - Depois, popule o vetor de dados com a função setDados().
    - Por fim, chame a função transmiteLinha().

    """

    def __init__(self, separador=";", usarProtocolo=True,  baudrate=57600, codificacao='UTF-8'):
        """Construtor: Inicializa parâmetros de configuração do Transmissor.
        Exitem dois métodos de transmissão, utilizando o protolo ou não.

        * Utilizando protocolo: As mensagens enviadas são empacotadas da seguinte forma:
        "!identificador=valor@\" onde o identificador é o "apelido" de cada dado.

        * Não utilizando protocolo: As mensagens são enviadas da mesma ordem que os dados são gravados.
        "valor1, valor2, valor3"


        :param separador: Especifica o tipo de separados dos valores mais comum é virgula espaço ou tabulação
        :param protocolo: Indica a utilização ou não do protocolo
        :param baudRate: Taxa de transmissão da serial
        :param codificacao: Tipo de codificação dos caracteres ASCII
        """
        self.dados = []
        self.separador = separador
        self.baudrate = baudrate
        self.usarProtocolo = usarProtocolo
        self.codificacao = codificacao
        self.transmissorEncontrado = False
        self.connect()

    def connect(self):
        print("########## Trying Transmissor! ##########")
        pts = prtlst.comports()
        for pt in pts:
            if 'USB' or 'ACM' in pt[0]:
                if 'FT' in pt[1]:
                    self.porta = pt[0]
                    self.devName = pt[1]
                    print('Connecting on Transmissor ' + self.devName + ' on port ' + self.porta)
                    self.serial = serial.Serial(port=self.porta, baudrate=self.baudrate, timeout=0.01)
                    self.transmissorEncontrado = True

    def transmiteLinha(self):
        """Função será chamada quando os dados deverão ser transmitidos.

        A forma de transmissão dependerá da utilização do protocolo ou não.
        Recomenda-se a utilização do protocolo para verificar a integridade do dado.
        """
        for dado in self.dados:
            if dado.transmiteDado:
                if self.usarProtocolo:
                    try:
                        string = '!{}={:.{prec}f}{sep}cks={:.{prec}f}@\n'.format(dado.apelido, dado.valor, dado.valor, prec=dado.casasDecimais, sep=self.separador)
                        self.serial.write(bytes(string, self.codificacao))
                    except:
                        pass
                else:
                    try:
                        string = '{:.{prec}f}\n'.format(dado.valor, prec=dado.casasDecimais)
                        self.serial.write(bytes(string, self.codificacao))
                    except:
                        pass

    def leLinha(self):
        """Essa função é responsável por ler telecomandos recebidos pela serial.

        :returns: String do telecomando
        """
        try:
            linhaLida = self.serial.readline().decode("utf-8")
            if(linhaLida != ""):
                linhaLida = linhaLida.replace('\n', '')
                return linhaLida
            else:
                return 'No command'
        except:
            pass

    def transmiteCru(self, data):
        try:
            string = '{:.4f}\n'.format(data)
            self.serial.write(bytes(string, self.codificacao))
        except:
            pass

    def transmiteDadoProtocolado(self, apelido, valor):
        try:
            string = '!{}={:.4f}{sep}cks={:.4f}@\n'.format(apelido, valor, valor, sep=self.separador)
            self.serial.write(bytes(string, self.codificacao))
        except:
            pass
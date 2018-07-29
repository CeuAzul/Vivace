#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import serial
import time
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

    def __init__(self, separador=",", usarProtocolo=True,  baudRate=57600, codificacao='UTF-8', porta='/dev/ttyUSB0'):
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
        self.baudRate = baudRate
        self.separador = separador
        self.usarProtocolo = usarProtocolo
        self.codificacao = codificacao
        self.porta = porta

        self.serial = serial.Serial(self.porta, self.baudRate, timeout=0.001)

    def setDados(self, dados):
        """Função que atualiza o vetor de dados do Transmissor com os dados que vem como parâmetro dessa função.
        O Transmissor apenas consegue ver os dados que foram passados por meio dessa função.
        É utilizada como a porta de entrada para os dados que serão escritos.

        :param d: Vetor de Dado que será escrito na ordem do vetor.
        """
        self.dados = dados

    def transmiteLinha(self):
        """Função será chamada quando os dados deverão ser transmitidos.

        A forma de transmissão dependerá da utilização do protocolo ou não.
        Recomenda-se a utilização do protocolo para verificar a integridade do dado.
        """
        for dado in self.dados:
            if dado.transmiteDado:
                if self.usarProtocolo:
                    try:
                        self.serial.write(
                            bytes("!" + dado.apelido + "=" + str(dado.valor) + "@\n", self.codificacao))
                    except:
                        pass
                else:
                    try:
                        self.serial.write(
                            bytes(str(dado.valor) + self.separador, self.codificacao))
                    except:
                        pass
        if not self.usarProtocolo:
            try:
                self.serial.write(bytes("\n", self.codificacao))
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
            self.serial.write(bytes(str(data), self.codificacao))
        except:
            pass

    def transmiteProtocolado(self, data):
        try:
            self.serial.write(bytes("!" + str(data) + "@\n", self.codificacao))
        except:
            pass

    def transmiteDadoProtocolado(self, apelido, valor):
        try:
            self.serial.write(bytes("!" + str(apelido) + "=" + str(valor) + "@\n", self.codificacao))
        except:
            pass
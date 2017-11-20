#!/usr/bin/python
# -*- coding: utf-8 -*-

import serial
import time
from .dado import Dado


class Transmissor:
    """ Esta classe é chamada toda vez que queremos transmitir um dado usando o transceiver da 3DR
    Depois de criar os dados, utiza-se a função setDados() para popular o vetor dessa classe com os
    dados a serem transmitidos.

    Para utilizar a classe:
    - Primeiramente utilize o construtor para setar propriedades.
    - Depois, popule o vetor de dados com a função setDados()
    - Por fim, chame a função transmiteLinha()

    """

    def __init__(self, separador=",", protocolo=True,  baudRate=57600, codificacao='UTF-8'):
        """Construtor inicializa parâmetros de configuração do Transmissor
        Exitem dois métodos de transmissão, utilizando o protolo ou não.

        Utilizando protocolo: As mensagens enviadas são empacotadas da seguinte forma:
        "!identificador=valor@\" onde o identificador é o "apelido" de cada dado.

        Não utilizando protocolo: As mensagens são enviadas da mesma ordem que os dados são gravados
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
        self.protocolo = protocolo
        self.codificacao = codificacao
        self.ser = serial.Serial('/dev/ttyUSB0', baudRate, timeout=0.001)

    def setDados(self, d):
        """Função que atualiza o vetor de dados do Transmissor com os dados que vem como parâmetro dessa função.
        O Transmissor apenas consegue ver os dados que foram passados por meio dessa função.
        É utilizada como a porta de entrada para os dados que serão escritos.

        :param d: Vetor de Dado que será escrito na ordem do vetor.
        """
        self.dados = d

    def transmiteLinha(self):
        """Função será chamada quando os dados deverão ser transmitidos

        A forma de transmissão dependerá da utilização do protocolo ou não
        Recomenda-se a utilização do protocolo para verificar a integridade do dado.

        """
        for x in self.dados:
            if x.transmiteDado:
                if self.protocolo:
                    self.ser.write(bytes("!" + x.apelido + "=" +
                                         str(x.valor) + "@\n", self.codificacao))
                else:
                    self.ser.write(
                        bytes(str(x.valor) + self.separador, self.codificacao))
        if not self.protocolo:
            self.ser.write(bytes("\n", self.codificacao))

    def leLinha(self):
        """Essa função é responsável por ler telecomandos recebidos pela serial

        :returns: String do telecomando
        """
        x = self.ser.readline().decode("utf-8")
        return x

#!/usr/bin/python
# -*- coding: utf-8 -*-

import os.path
import os
import datetime
import shutil
from shutil import copytree, ignore_patterns
from .dado import Dado


class Escritor:
    """É responsável pela escrita dos dados em um arquivo de texto.
    Esta classe será chamada toda vez que queremos gravar os valores
    que estão sendo adquirido pelos sensores em um arquivo de texto.

    A classe pode ser modificada das seguintes maneiras:

    * Indicar o tipo de separador dos dados (virgula, espaço, tabulação etc..).
    * Se deve colocar o nome dos dados na primeira linha.
    * Se deve colocar a unidade de medida na segunda linha.
    * Nome do arquivo.
    * Extensão do arquivo.

    Para utilizar a classe seguimos os seguintes passos:

    1. Inicializamos a classe configurando o escritor para criar o arquivo do jeito que quisermo.
    2. Chamamos a função setDado com um vetor de objetos criados da classe "Dado", já com nome e unidade de medida.
    3. Quando quisermos que a gravação de dados inicie, devemos chamar "fazCabecalho()".
    4. Cada vez que quiser que o Escritor grave uma linha dado, primeiro atualize o vetor de dados "setDados()" e depois invoque "escreveLinhaDado(self)".
    5. Veja o dado sendo gravado e corra para o abraço.

    Multiplos inicializações são criadas arquivos com o mesmo nome, mas com número diferente ex:

    - Nome arquivo - 01.
    - Nome arquivo - 02.
    - Nome arquivo - 03.
    - ...
    """

    def __init__(self, configurador, separador=",", printaNome=True, printaUM=True, printaInfos=True, nomeArquivo="Telemetria", extensao=".csv", pasta= os.path.join(os.path.dirname(__file__), 'Dados')):
        """Construtor: Inicializa parâmetros de configuração do Escritor.
        No construtor ele já cria o arquivo, verifica se nome já existe, caso já exista, adiciona 1 no nome.

        :param separador: Especifica o tipo de separados dos valores mais comum é virgula espaço ou tabulação
        :param printaNome: Indicador se deve ser gravado o nome do dado na primeira linha do cabeçalho
        :param printaUM: Indicador se deve ser gravado a unidade de medida na segunda linha do cabeçalho
        :param nomeArquivo: Nome do arquivo
        :param extensao: Extensão do arquivo a ser criado
        """

        self.dados = []  # vetor de Dado()
        self.separador = separador
        self.printaNome = printaNome
        self.printaUM = printaUM
        self.printaInfos = printaInfos
        self.nomeArquivo = nomeArquivo
        self.pasta = pasta
        self.extensao = extensao
        self.numeroArquivo = 1
        self.configurador = configurador
        self.dataHora = datetime.datetime.now().strftime("%d-%m-%y %H:%M")
        for file in os.listdir(self.pasta):
            if file.startswith(self.nomeArquivo):
                self.numeroArquivo +=1
        self.nomeCompleto = self.pasta + "/" + \
                            self.nomeArquivo + " " + \
                            str(self.numeroArquivo) + " - " + \
                            "(" + self.dataHora + ")" + \
                            self.extensao

    def addDado(self, dados):
        """Adiciona um dado no vetor de dados.

        :param d: Dado a ser adicionado.
        """
        self.dados.append(dados)

    def verificaTamanhoArquivo(self):
        """Retorna o tamanho do arquivo.
        """
        try:
            b = (os.path.getsize(self.nomeCompleto) / 1000000)
            return b
        except Exception as e:
            print(e)
            return -1

    def fazCabecalho(self):
        """Escreve o cabeçalho do arquivo:

        * Se printaNome=True -> Printa o nome dos dados na primeira linha.
        * Se printaUM=True -> Printa unidade de medida na segunda linha.
        """
        os.makedirs(os.path.dirname(self.nomeCompleto), exist_ok=True)
        with open(self.nomeCompleto, "a") as file:
            if self.printaInfos:
                file.write('Nome da aeronave: ' + self.configurador.NOME_DA_AERONAVE + '\r\n')
                file.write('Local de voo: ' + self.configurador.LOCAL_DE_VOO + '\r\n')
                file.write('Temperatura: ' + self.configurador.TEMPERATURA + '\r\n')
                file.write('Angulo de incidencia da asa: ' + self.configurador.ANGULO_INCIDENCIA_ASA + '\r\n')
                file.write('Angulo de incidencia do profundor: ' + self.configurador.ANGULO_INCIDENCIA_PROFUNDOR + '\r\n')
                file.write('Informaçoes extras: ' + self.configurador.INFOS_EXTRAS + '\r\n')
            if self.printaNome:
                for dado in self.dados:
                    if dado.gravaDado:
                        string = '{}{sep}'.format(dado.nome, sep=self.separador)
                        file.write(string)
            file.write("\r\n")
            if self.printaUM:
                for dado in self.dados:
                    if dado.gravaDado:
                        string = '{}{sep}'.format(dado.unidadeMedida, sep=self.separador)
                        file.write(string)
            file.write("\r\n")

    def escreveLinhaDado(self):
        """Função que escreve a linha com os valores atuais do dado separado pelo separador.

           Antes de gravar, a função verifica se o dado é mesmo para ser gravado ou não.
        """
        os.makedirs(os.path.dirname(self.nomeCompleto), exist_ok=True)
        with open(self.nomeCompleto, "a") as file:
            for dado in self.dados:
                if dado.gravaDado:
                    if type(dado.valor) == float:
                        string = '{:.{prec}f}{sep}'.format(dado.valor, prec=dado.casasDecimais, sep=self.separador)
                        file.write(string)
                    else:
                        string = '{}{sep}'.format(dado.valor, sep=self.separador)
                        file.write("%s%s" % (dado.valor, self.separador))
            file.write("\r\n")

    def passaProPendrive(self):
        nomesPastas = os.listdir("/media/pi")
        try:
            for pen in nomesPastas:
                if pen != "SETTINGS":
                    d = datetime.datetime.now().strftime(
                        '%d%m%Y_%H%M%S%f')[:-3]
                    source = self.pasta
                    destination = '/media/pi/%s/Telemetria/Dados_%s' % (pen, d)
                    copytree(source, destination)
        except Exception as e:
            print(e)

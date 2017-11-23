#!/usr/bin/python
# -*- coding: utf-8 -*-

class Dado:
    """Esta classe é criada com o objetivo de servir como objeto para um dado.
    Cada dado será uma instância dessa classe e terá o mesmo padrão de atributos.

    Cada vez que atualizarmos os sensores, iremos setar o valor do dado para
    o ultimo valor captado pelo sensor, dessa forma, sabemos exatamente o valor
    atual do dado.
    """

    def __init__(self, nome, unidadeMedida, apelido, gravaDado=True, transmiteDado=False, printaDado=False, casasDecimais=3):
        """Construtor: Inicializa as variáveis necessárias.

        :param name: Nome completo do dado
        :param unidadeMedida: Unidade de medida do dado
        :param apelido: Identificador de letras utilizado na transmissão de dados
        :param gravaDado: Indicador se o dado deve ser gravado no arquivo ou não
        :param transmiteDado: Indicador se o dado deve ser transmitido ou não
        :param printaDado: Indicador se o dado deve ser exibido na tela ou não
        :param casasDecimais: Indica quantas casas decimais o número deve ter depois da virgula para ser escrito e transmitido

        """
        self.nome = nome
        self.unidadeMedida = unidadeMedida
        self.apelido = apelido  # Deve conter 3 letras/numeros
        self.gravaDado = gravaDado
        self.transmiteDado = transmiteDado
        self.printaDado = printaDado
        self.valor = 0
        self.casasDecimais = casasDecimais

    def setValor(self, valor):
        """Função seta o valor atual da variável para a especificada no parâmetro.

        :param valor: Valor atual do dado
        """
        # Filtrar dado aqui
        self.valor = valor

    def getValor(self):
        """Retorna o valor atual do dado.

        :returns: Valor atual do dado
        """
        return self.valor

    def setTransmissao(self, mode):
        """Indica se dado deve ser transmitido ou não.

        :param mode: Boolean indicando se deve ser transmitido ou não
        """
        self.transmiteDado = mode

    def setGravacao(self, mode):
        """Indica se dado deve ser gravado ou não.

        :param mode: Boolean indicando se deve ser gravado ou não
        """
        self.gravaDado = mode

    def setPrintDado(self, mode):
        """Indica se dado deve ser exibido na tela ou não.

        :param mode: Boolean indicando se deve ser exibido ou não
        """
        self.printDado = mode

#!/usr/bin/python
# -*- coding: utf-8 -*-

class Dado:
    """Esta classe é criada com o objetivo de servir como objeto para um dado.
    Cada dado será uma instância dessa classe e terá o mesmo padrão de atributos.

    Cada vez que atualizarmos os sensores, iremos setar o valor do dado para
    o ultimo valor captado pelo sensor, dessa forma, sabemos exatamente o valor
    atual do dado.
    """

    def __init__(self, nome, unidadeMedida, apelido, sensor="", casasDecimais=3, isCru=False, isUtil=False, gravaDado=True, transmiteDado=False, printaDado=False):
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
        self.sensor = sensor
        self.isCru = isCru
        self.isUtil = isUtil

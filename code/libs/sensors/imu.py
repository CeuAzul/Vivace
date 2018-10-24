#!/usr/bin/python
# -*- coding: utf-8 -*-

class IMU:
    """
    Um objeto dessa classe deve ser criado quando quiser realizar a comunicação
    ou obter dados da MPU (Acelerômetro e Giroscópio).
    Para utilizar a classe, criamos o construtor colocando como parâmetros
    se queremos pegar os parâmetros. Depois, utilizamos a função
    atualiza() para fazer a aquisição pelo I2C. Por fim, acessa os dados
    usando os getters().
    """

    def __init__(self, arduino):
        """Inicializa a classe com os parâmetros setados para adquirir e
        realiza configurações para aquisição do I2C.
        """
        self.gyx = 0
        self.gyy = 0
        self.gyz = 0
        self.acx = 0
        self.acy = 0
        self.acz = 0
        self.prs = 0
        self.temp = 0
        self.arduino = arduino

    def atualiza(self):
        """Le valor analogico do ADC e transforma isso em pressão e
        velocidade. Todas as variaveis sao entao atualizadas.

        :param samples: Número de amostras para oversampling
        :param densAr: Densidade local do ar
        """

        dicioDeDados = self.arduino.dicioDeDados
        if 'acx' in dicioDeDados:
            self.acx = dicioDeDados['acx']
        if 'acy' in dicioDeDados:
            self.acy = dicioDeDados['acy']
        if 'acz' in dicioDeDados:
            self.acz = dicioDeDados['acz']
        if 'gyx' in dicioDeDados:
            self.gyx = dicioDeDados['gyx']
        if 'gyy' in dicioDeDados:
            self.gyy = dicioDeDados['gyy']
        if 'gyz' in dicioDeDados:
            self.gyz = dicioDeDados['gyz']

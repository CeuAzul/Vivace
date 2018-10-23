import os

class Configurador(object):

    def __init__(self):

        # GERAIS
        self.NOME_DO_ARQUIVO = 'Bancada'
        self.PASTA_DESTINO = os.path.expanduser('~/Documents/DadosBancada')

        self.LISTA_SENSORES = ['GERAL', 'ARDUINO', 'IMU', 'GPS', 'BARO', 'PITOT', 'SONDA_AOA', 'CELULA', 'BALANCA']

        self.LISTA_USAR = ['GERAL', 'ARDUINO', 'IMU', 'GPS', 'BARO', 'PITOT', 'SONDA_AOA', 'CELULA', 'BALANCA']
        self.LISTA_GRAVAR = ['GERAL', 'ARDUINO', 'IMU', 'GPS', 'BARO', 'PITOT', 'SONDA_AOA', 'CELULA', 'BALANCA']
        self.LISTA_TRANSMITIR = ['GERAL', 'ARDUINO', 'IMU', 'GPS', 'BARO', 'PITOT', 'SONDA_AOA', 'CELULA', 'BALANCA']

        self.ENVIAR_SINAL_DE_VIDA = True
        self.ATIVAR_TRANSMISSAO = True
        self.ATIVAR_GRAVACAO = True

        # PITOTS
        self.NUMERO_DE_PITOTS = 4
        self.NOME_DOS_PITOTS = ['Pitot 0', 'Pitot 1', 'Pitot 2', 'Pitot 3', 'Pitot 4', 'Pitot 5', 'Pitot 6', 'Pitot 7']
        self.APELIDO_DOS_PITOTS = ['pt0', 'pt1', 'pt2', 'pt3', 'pt4', 'pt5', 'pt6', 'pt7']

        self.CALFACTS_DOS_PITOTS = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]

        # SONDAS_AOA
        self.NUMERO_DE_SONDAS_AOA = 1

        self.NOME_DAS_SONDAS_AOA = ['Sonda AoA 0']

        self.APELIDO_DAS_SONDAS_AOA = ["aoa0"]

        self.CALFACTS_DAS_SONDAS_AOA = [[5.0, 0.834]]

        self.APELIDO_PITOTS_AOA = [['pt3', 'pt2']]

        # CELULAS
        self.NUMERO_DE_CELULAS = 5

        self.NOME_DAS_CELULAS = ['Celula Horizontal', 'Celula Frontal Direita', 'Celula Frontal Esquerda', 'Celula Traseira Direita', 'Celula Traseira Esquerda']

        self.APELIDO_DAS_CELULAS = ["fh", "ffd", "ffe", "ftd", "fte"]

        self.CALFACTS_DAS_CELULAS = [64100.0, 22100.0, 19600.0, 21500.0, 21400.0]

        # CONFIGURACOES DE TESTE
        self.NOME_DA_AERONAVE = 'Aeronave de teste'
        self.LOCAL_DE_VOO = 'Local de teste'
        self.TEMPERATURA = 'NaN'
        self.ANGULO_INCIDENCIA_ASA = 'NaN'
        self.ANGULO_INCIDENCIA_PROFUNDOR = 'NaN'
        self.INFOS_EXTRAS = 'N/A'
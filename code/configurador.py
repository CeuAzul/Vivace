import os

class Configurador(object):

    def __init__(self):

        # GERAIS
        self.NOME_DO_ARQUIVO = 'Bancada'
        self.PASTA_DESTINO = os.path.expanduser('~/Documents/DadosBancada')
        self.ARDUINO_PORT = '/dev/ttyACM0'
        self.TRANSMISSOR_PORT = '/dev/ttyUSB0'

        self.ATIVAR_TRANSMISSAO = True
        self.ATIVAR_GRAVACAO = True

        # IMU
        self.USAR_IMU = True
        self.GRAVAR_IMU = True
        self.TRANSMITIR_IMU = True

        # GPS
        self.USAR_GPS = True
        self.GRAVAR_GPS = True
        self.TRANSMITIR_GPS = True

        # BARO
        self.USAR_BARO = True
        self.GRAVAR_BARO = True
        self.TRANSMITIR_BARO = True

        # PITOTS
        self.USAR_PITOTS = True
        self.GRAVAR_PITOTS= True
        self.TRANSMITIR_PITOTS = True
        self.NUMERO_DE_PITOTS = 4
        self.NOME_DOS_PITOTS = [
            'Pitot 0',
            'Pitot 1',
            'Pitot 2',
            'Pitot 3',
            'Pitot 4',
            'Pitot 5',
            'Pitot 6',
            'Pitot 7',
            'Pitot 8',
            'Pitot 9',
            'Pitot 10',
            'Pitot 11',
            'Pitot 12',
            'Pitot 13',
            'Pitot 14',
            'Pitot 15'
        ]
        self.APELIDO_DOS_PITOTS = [
            'pt0',
            'pt1',
            'pt2',
            'pt3',
            'pt4',
            'pt5',
            'pt6',
            'pt7',
            'pt8',
            'pt9',
            'pt10',
            'pt11',
            'pt12',
            'pt13',
            'pt14',
            'pt15'
        ]

        self.CALFACTS_DOS_PITOTS = [
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0
        ]

        # SONDAS_AOA
        self.USAR_SONDAS_AOA = True
        self.GRAVAR_SONDAS_AOA = True
        self.TRANSMITIR_SONDAS_AOA = True
        self.NUMERO_DE_SONDAS_AOA = 1

        self.NOME_DAS_SONDAS_AOA = [
            'Sonda AoA 0'
        ]

        self.APELIDO_DAS_SONDAS_AOA = [
            "aoa0"
        ]

        self.CALFACTS_DAS_SONDAS_AOA = [
            [5.0, 0.834]
        ]

        self.APELIDO_PITOTS_AOA = [
            ['pt3', 'pt2']
        ]

        # CELULAS
        self.USAR_CELULAS = True
        self.GRAVAR_CELULAS= True
        self.TRANSMITIR_CELULAS = True
        self.NUMERO_DE_CELULAS = 5

        self.NOME_DAS_CELULAS = [
            'Celula Horizontal',
            'Celula Frontal Direita',
            'Celula Frontal Esquerda',
            'Celula Traseira Direita',
            'Celula Traseira Esquerda'
        ]

        self.APELIDO_DAS_CELULAS = [
            "fh",
            "ffd",
            "ffe",
            "ftd",
            "fte"
        ]

        self.CALFACTS_DAS_CELULAS = [
            64100.0,
            22100.0,
            19600.0,
            21500.0,
            21400.0
        ]

        # ARDUINO
        self.USAR_ARDUINO = True

        # BALANCA
        self.USAR_BALANCA = True

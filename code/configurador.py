class Configurador(object):

    def __init__(self):

        # GERAIS
        self.NOME_DO_ARQUIVO = 'Global'
        self.PASTA_DESTINO = '/home/rafael/Documents/DadosTelemetria'
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

        # ARDUINO
        self.USAR_ARDUINO = True

        # BALANCA
        self.USAR_BALANCA = True

        if os.uname()[1] != 'raspberrypi':
            configurador.USAR_BARO = False
            configurador.USAR_IMU = False
            configurador.USAR_GPS = False
            configurador.ATIVAR_TRANSMISSAO = False
            print("Rodando programa fora do RaspberryPi. Desativando Barometro, IMU, GPS, Pitots e Transmissao.")
class Configurador(object):

    def __init__(self):

        # GERAIS
        self.PASTA_DESTINO = '/home/rafael/Documents/DadosTelemetria'

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
            'pitot0',
            'pitot1',
            'pitot2',
            'pitot3',
            'pitot4',
            'pitot5',
            'pitot6',
            'pitot7',
            'pitot8',
            'pitot9',
            'pitot10',
            'pitot11',
            'pitot12',
            'pitot13',
            'pitot14',
            'pitot15'
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

        # ARDUINONANO
        self.USAR_ARDUINO = True

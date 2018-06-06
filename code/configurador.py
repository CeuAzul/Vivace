class Configurador(object):

    def __init__(self):

        # GERAIS
        self.PASTA_DESTINO = '/home/rafael/Documents'

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
            'Pitot 15',
            'Pitot 16'
        ]
        self.APELIDO_DOS_PITOTS = [
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
            'pitot15',
            'pitot16'
        ]

        # CELULAS
        self.USAR_CELULAS = True
        self.GRAVAR_CELULAS= True
        self.TRANSMITIR_CELULAS = True

        # NANO
        self.USAR_NANO = True


        print('Dados gerais criados')

        self.tempo = Dado("Tempo", "seg", "tmp", "GERAL", 4)
        self.mensagemRecebida = Dado("Mensagem", "str", "msg" "GERAL")
        self.modo = Dado("Modo", "int", "mod", "GERAL")
        self.tamanho = Dado("Tamanho do arquivo", "int", "tmn", "GERAL", 3)

        print('Dados da IMU criados!')

        self.taxaGiroX = Dado("Taxa de giro em X", "º/s", "gyx", "IMU", 2)
        self.taxaGiroY = Dado("Taxa de giro em Y", "º/s", "gyy", "IMU", 2)
        self.taxaGiroZ = Dado("Taxa de giro em Z", "º/s", "gyz", "IMU", 2)
        self.aceleracaoX = Dado("Aceleração em X", "g", "acx", "IMU", 2)
        self.aceleracaoY = Dado("Aceleração em Y", "g", "acy", "IMU", 2)
        self.aceleracaoZ = Dado("Aceleração em Z", "g", "acz", "IMU", 2)
        self.pitch = Dado("Pitch", "º", "pit", "IMU", 2)
        self.roll = Dado("Roll", "º", "rol", "IMU", 2)

        print('Dados do BARO criados!')

        self.pressaoTotal = Dado("Pressao total", "PA", "ptt", "BARO", 3)
        self.pressaoEstatica = Dado("Pressao estática", "PA", "pts", "BARO", 3)
        self.pressaoTotalr = Dado("PTtotal", "PA", "ptt", "BARO", 3)
        self.pressaoEstaticar = Dado("PTstatic", "PA", "psr", "BARO", 3)
        self.temperaturaBar = Dado("Temperatura", "ºC", "tem", "BARO", 3)
        self.densidadeAr = Dado("Densidade do ar", "Kg/m³", "den", "BARO", 3)
        self.altitudeRelativa = Dado("Altitude relativa", "m", "alt", "BARO", 3)
        self.altitudePressao = Dado("HP", "ft", "hps", "BARO", 3)

        print('Dados do GPS criados!')

        self.dadoTempoGPS = Dado("Tempo GPS", "-", "tmg", "GPS", 3)
        self.latitude = Dado("Latitude", "º", "lat", "GPS", 6)
        self.longitude = Dado("Longitude", "º", "lng", "GPS", 6)
        self.altitude = Dado("ZGPS", "m", "atg", "GPS", 2)
        self.direcaoCurso = Dado("Direção de curso", "º", "cog", "GPS", 1)
        self.velocidade = Dado("Velocidade GPS", "m/s", "vel", "GPS", 2)
        self.velocidadeSubida = Dado("Velocidade de subida", "m/s","ves", "GPS", 2)
        self.erroX = Dado("Erro em X", "m", "erx", "GPS", 1)
        self.erroY = Dado("Erro em Y", "m", "ery", "GPS", 1)
        self.erroAltitude = Dado("Erro da altitude", "m", "era", "GPS", 1)
        self.erroVelocidade = Dado("Erro de velocidade", "nós", "ers", "GPS", 1)
        self.erroVelocidadeSubida = Dado("Erro da velocidade de subida", "m/s", "ves", "GPS", 1)
        self.nivelFixacao = Dado("Nivel de fixação GPS", "-", "nfx", "GPS", 1)
        self.latitudeRef = Dado("Latitude de referência", "-", "ltr", "GPS", 6)
        self.longitudeRef = Dado("Longitude de referência", "-", "lgr", "GPS", 6)
        self.posicaoX = Dado("XGPS", "m", "gpx", "GPS", 2)
        self.posicaoY = Dado("YGPS", "m", "gpy", "GPS", 2)
        self.distanciaAbsoluta = Dado("Distancia absoluta", "m", "dtr", "GPS", 2)

        print('Dados dos PITOTS criados!')

        nomeDosPitots = self.configurador.NOME_DOS_PITOTS
        apelidoDosPitots = self.configurador.APELIDO_DOS_PITOTS

        self.pressaoDin = []
        self.velCas = []

        for pitot in range(self.configurador.NUMERO_DE_PITOTS):
            print(nomeDosPitots[pitot] + ' criado!')
            self.pressaoDin.extend([Dado("Pressao Dinamica - " + nomeDosPitots[pitot], "PA", apelidoDosPitots[pitot], "PITOT", 3)])
            self.velCas.extend([Dado("VCAS - " + nomeDosPitots[pitot], "m/s", "vcs_" + apelidoDosPitots[pitot], "PITOT", 4)])

        print('Dados das CELULAS criados!')

        nomeDasCelulas = self.configurador.NOME_DAS_CELULAS
        apelidoDasCelulas = self.configurador.APELIDO_DAS_CELULAS

        self.Lift = Dado("Lift", "N", "lft", "CELULA", 3)
        self.Drag = Dado("Drag", "N", "drg", "CELULA", 3)
        self.Moment = Dado("Moment", "N", "mmt", "CELULA", 3)
        self.DistCp = Dado("Distance Cp", "m", "dcp", "CELULA", 3)

        self.forcas = []
        for celula in range(self.configurador.NUMERO_DE_CELULAS):
            print(nomeDasCelulas[celula] + ' criada!')
            self.forcas.extend([Dado("Forca - " + nomeDasCelulas[celula], "N", apelidoDasCelulas[celula], "CELULA", 3)])

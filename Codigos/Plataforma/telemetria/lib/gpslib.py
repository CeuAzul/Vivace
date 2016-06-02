from .GPSController import GpsController
from math import radians, cos, sin, asin, sqrt
NaN = float('nan')
MODE_NO_FIX = 1
MODE_2D = 2
MODE_3D = 3
class Gps:
        """
        Esta classe é o conjunto de funções relaciodas a aquisição de dados do GPS
        Para utiliza-la, basta criar o objeto GPS e de tempos em tempos, chamar
        a função atualizaGps(). Essa função irá pegar os ultimos dados recebidos
        dos satélites e irá preencher as variáveis com estes dados. Para pegar
        esses valores, basta usar os getters disponíveis.

        Note o seguinte: Esta função utiliza uma outra classe chamada GPSController
        que ajudar a fazer a gerência das informações. Nessa classe, é criada uma thread
        que irá constantemente pegar as informações vindas do satélite, precessar e
        pegar os dados. Essa thread pode ser entendida como um processo separado, ou
        seja, mesmo que não estamos vendo, há um processo sendo executado no fundo, fazendo
        a aquisição dos dados do gps. Essa classe (Gps) é usada apenas para pegar os dados
        processados do GpsController e adicionar para as variáveis da classe (tal como uma
        interface entre a classe GpsController e o código global).
        
        """

    def haversine(self, lon1, lat1, lon2, lat2):
        """
        Calcula a distância em metros entre dois pontos de coodenadas de latitude e longitude

        :param lon1: Valor da longitude 1
        :param lat1: Valor da latitude 1
        :param lon2: Valor da longitude 2
        :param lat2: Valor da latitude 2
        :returns: Distância em metros entre os pontos
        """
        # convert decimal degrees to radians 
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        # haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        km = 6367 * c
        metros = km*1000
        return metros

    def __init__(self):
        """
        Construtor, utilizado apenas para inicializar variáveis.
        """
        self.latitude = 0
        self.erroY = 0
        self.longitude = 0
        self.erroX = 0
        
        self.tempo = NaN
        self.utc = NaN
        self.erroTempo = NaN

        self.altitude = 0
        self.erroAltitude = 0

        self.direcaoCurso = 0
        self.erroDirecao = 0

        self.velocidade = 0
        self.erroVelocidade = 0

        self.velSubida = 0
        self.erroVelSubida = 0

        self.nivelFixacao = MODE_NO_FIX

        self.latitudeRef = 0
        self.longitudeRef = 0

        self.posicaoX = 0
        self.posicaoY = 0
        self.distanciaAbsoluta = 0
        
        #create controller
        self.gpsc = GpsController() 
        #start controller
        self.gpsc.start()

        

    def atualiza(self):
        """ Essa função atualiza as variáveis relacionadas ao GPS. Chame-a
        toda vez que quiser passar as ultimas informações procesadas dos
        satélites para as variáveis dessa classe.
        
        """
        self.latitude = self.gpsc.fix.latitude
        self.erroY = self.gpsc.fix.epy
        self.longitude = self.gpsc.fix.longitude
        self.erroX = self.gpsc.fix.epx
        self.tempo = self.gpsc.fix.time
        self.utc = self.gpsc.utc
        self.erroTempo = self.gpsc.gpsd.fix.ept
        self.altitude = self.gpsc.fix.altitude
        self.erroAltitude = self.gpsc.fix.epv
        self.direcaoCurso = self.gpsc.fix.track
        self.velocidade = self.gpsc.fix.speed
        self.erroVelocidade = self.gpsc.fix.eps
        self.velSubida = self.gpsc.fix.climb
        self.erroVelSubida = self.gpsc.fix.epc
        self.nivelFixacao = self.gpsc.fix.mode
        if(self.latitudeRef == 0 or self.longitudeRef == 0):
            self.setReferenciaAqui()
        else:
            if((self.latitude < 90 and self.latitude > -90) and self.latitude != 0):
                self.posicaoY = self.haversine(0, self.latitudeRef, 0, self.latitude)
            if((self.longitude < 360 and self.longitude > -360) and self.longitude != 0):
                self.posicaoX = self.haversine(self.longitudeRef, 0, self.longitude, 0)
            if((self.longitude < 360 and self.longitude > -360) and self.longitude != 0):
                if((self.latitude < 90 and self.latitude > -90) and self.latitude != 0):
                    self.distanciaAbsoluta = self.haversine(self.longitudeRef, self.latitudeRef, self.longitude, self.latitude)

    def setReferenciaAqui(self):
        """ Esta função pega os ultimo dado de latitude e longitude e coloca
        como referência. Esta referência será utilizada para saber a distância
        em metros que o avião está, ou seja, será utilizada como (0,0) no plano
        cartesiano.

        :returns: Se deu certo colocar este ponto como referência.
        """
        deuCertoLat = False
        deuCertoLong = False
        if((self.latitude < 90 and self.latitude > -90) and self.latitude != 0):
            self.latitudeRef = self.latitude
            deuCertoLat = True
        if((self.longitude < 360 and self.longitude > -360) and self.longitude != 0):
            self.longitudeRef = self.longitude
            deuCertoLong = True
        return (deuCertoLat and deuCertoLong)
                
    def finaliza(self):
        """ Após a aquisição de dado, precisa-se parar a interpretação dos dados
        pelo gpsc. Por isso chamamos essa função, caso contrário, ele ficará
        realizando o processo indefinidamente.
        """
        #stop controller
        self.gpsc.stopController()

    def getLatitude(self):
        """ Retorna a latitude atual.
        :returns:Latitude atual.
        """
        return self.latitude

    def getErroY(self):
        """ Retorna o erro em metros do eixo de latitude.
        :returns: Erro no eixo Y.
        """
        return self.erroY

    def getLongitude(self):
        """Retorna Longitude atual.
        :returns: Longitude atual.
        """
        return self.longitude

    def getErroX(self):
        """ Retorna o erro em metros do eixo de longitude.
        :returns: Erro no eixo X.
        """
        return self.erroX

    def getTempo(self):
        """Retorna tempo atual.
        :returns: Tempo atual.
        """
        return self.tempo

    def getErroTempo(self):
        """
        :returns: Erro do tempo atual.
        """
        return self.erroTempo

    def getUTC(self):
        """Pega o tempo atual em UTC
        :returns: Tempo atual em UTC.
        """
        return self.utc

    def getAltitude(self):
        """Pega altitude atual vinda do gps
        :returns: Altitude atual
        """
        return self.altitude

    def getErroAltitude(self):
        """Pega o erro de altitude.
        :returns: Erro atual de altitude
        """
        return self.erroAltitude

    def getDirecaoCurso(self):
        """Pega direção de curso do avião (direção da velocidade que o avião ta indo
        semelhante ao yaw.
        :returns: Direção de curso
        """
        return self.direcaoCurso

    def getVelocidade(self):
        """Pega velocidade atual do avião.
        :returns: Velocidade em m/s (?)
        """
        return self.velocidade

    def getErroVelocidade(self):
        """Pega erro de velocidade.
        :returns: Erro de velocidade
        """
        return self.erroVelocidade

    def getVelSubida(self):
        """Velocidade vertical do avião.
        :returns: Velocidade vertical
        """
        return self.velSubida

    def getErroVelSubida(self):
        """Pega erro de velocidade atual do avião.
        :returns: Erro de velocidade vertical.
        """
        return self.erroVelSubida

    def getNivelFixacao(self):
        """Pega em que dimensão o satélite está com lock.
        MODE_NO_FIX = 1 (Não pegou satélite)
        MODE_2D = 2 (Pegando apenas latitude e longitude)
        MODE_3D = 3 (Pegando latitude, longitude e altitude)
        :returns: Nível de fixação (1 = não fixo, 2 = 2d, 3 = 3d).
        """
        return self.nivelFixacao

    def getLatitudeRef(self):
        """Pega a latitude de referência (latitude que será considerada
        o ponto zero no plano, apartir desse ponto será calculada a distância
        x e y)
        :returns: Latitude de referência.
        """
        return self.latitudeRef

    def getLongitudeRef(self):
        """Pega a longitude de referência (lopngitude que será considerada
        o ponto zero no plano, apartir desse ponto será calculada a distância
        x e y)
        :returns: Longitude de referência.
        """
        return self.longitudeRef

    def getPosicaoX(self):
        """Pega a distância X em metros apartir de um ponto de referência (latitude e longitude de referência)
        :returns: Posição X do avião em metros.
        """
        return self.posicaoX

    def getPosicaoY(self):
        """Pega a distância Y em metros apartir de um ponto de referência (latitude e longitude de referência)
        :returns: Posição Y do avião em metros.
        """
        return self.posicaoY

    def getDistanciaAbsoluta(self):
        """ Pega distância absoluta apartir do ponto de referência
        :returns: Distância absoluta apartir do ponto de referência
        """
        return self.distanciaAbsoluta



    
        



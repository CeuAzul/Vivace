#!/usr/bin/python
import smbus
import math

class MPU:
"""
Um objeto dessa classe deve ser criado quando quiser realizar a comunicação
ou obter dados da MPU (Acelerômetro e Giroscópio). 
Para utilizar a classe, criamos o construtor colocando como parâmetros
se queremos pegar os parâmetros. Depois, utilizamos a função
atualiza() para fazer a aquisição pelo I2C. Por fim, acessa os dados
usando os getters().
"""
    def __init__(self, useGyx=True, useGyy=True, useGyz = True, useAcx=True, useAcy=True, useAcz=True, usePitch=True, useRoll=True, useTemp=True):
        """Inicializa a classe com os parâmetros setados para adquirir e
        realiza configurações para aquisição do I2C.
        :param useGyx: Indicador se deve adquirir a taxa de rotação no eixo X
        :param useGyy: Indicador se deve adquirir a taxa de rotação no eixo y
        :param useGyz: Indicador se deve adquirir a taxa de rotação no eixo Z
        :param useAcx: Indicador se deve adquirir a aceleração no eixo X
        :param useAcy: Indicador se deve adquirir a aceleração no eixo Y
        :param useAcz: Indicador se deve adquirir a aceleração no eixo Z
        :param usePitch: Indicador se deve adquirir Pitch
        :param useRoll: Indicador se deve adquirir Roll
        :param useTemp: Indicador se deve adquirir Temperatura
        """
        self.useGyx = useGyx
        self.useGyy = useGyy
        self.useGyz = useGyz
        self.useAcx = useAcx
        self.useAcy = useAcy
        self.useAcz = useAcz
        self.usePitch = usePitch
        self.useRoll = useRoll
        self.useTemp = useTemp
        self.gyx = 0
        self.gyy = 0
        self.gyz = 0
        self.acx = 0
        self.acy = 0
        self.acz = 0
        self.pitch = 0
        self.roll = 0
        self.temp = 0
        
        self.bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
        # Power management registers
        self.power_mgmt_1 = 0x6b
        self.power_mgmt_2 = 0x6c
        self.gyRegScale = 0x1b
        self.acRegScale = 0x1c  
        self.address = 0x68       # This is the address value read via the i2cdetect command
        # Now wake the 6050 up as it starts in sleep mode
        self.bus.write_byte_data(self.address, self.power_mgmt_1, 0)
        self.bus.write_byte_data(self.address, self.gyRegScale, 0b00001000)
        self.bus.write_byte_data(self.address, self.acRegScale, 0b00010000)

    def read_byte(self, adr):
        """Função apenas para uso interno na comunicação i2c.
        """
        return self.bus.read_byte_data(self.address, adr)

    def read_word(self, adr):
        """Função apenas para uso interno na comunicação i2c.
        """
        high = self.bus.read_byte_data(self.address, adr)
        low = self.bus.read_byte_data(self.address, adr+1)
        val = (high << 8) + low
        return val

    def read_word_2c(self, adr):
        """Função apenas para uso interno na comunicação i2c.
        """
        val = self.read_word(adr)
        if (val >= 0x8000):
            return -((65535 - val) + 1)
        else:
            return val

    def dist(self, a,b):
        """Função apenas para uso interno na comunicação i2c.
        """
        return math.sqrt((a*a)+(b*b))
    
    def get_y_rotation(self, x,y,z):
        """Função apenas para uso interno na obtenção do pitch e roll.
        """
        radians = math.atan2(x, self.dist(y,z))
        return -math.degrees(radians)
    
    def get_x_rotation(self, x,y,z):
        """Função apenas para uso interno na obtenção do pitch e roll.
        """
        radians = math.atan2(y, self.dist(x,z))
        return math.degrees(radians)
    
    def atualiza(self):
        """Função que atualiza todos os dados da MPU (faz a comunicação i2c
        e atualiza as variaveis locais)
        """
        if self.useGyx:
            gyro_xout = self.read_word_2c(0x43)
            self.gyx = gyro_xout / 65.5
        if self.useGyy:
            gyro_yout = self.read_word_2c(0x45)
            self.gyy = gyro_yout / 65.5
        if self.useGyz:
            gyro_zout = self.read_word_2c(0x47)
            self.gyz = gyro_zout / 65.5
            
        if self.useAcx:
            accel_xout = self.read_word_2c(0x3b)
            accel_xout_scaled = accel_xout / 4096
            self.acx = accel_xout_scaled
        if self.useAcy:
            accel_yout = self.read_word_2c(0x3d)
            accel_yout_scaled = accel_yout / 4096
            self.acy = accel_yout_scaled
        if self.useAcz:
            accel_zout = self.read_word_2c(0x3f)
            accel_zout_scaled = accel_zout / 4096
            self.acz = accel_zout_scaled
            
        if self.useTemp:
            temp_out = self.read_word_2c(0x41)
            self.temp = temp_out/340+36.53
            
        if self.usePitch:
            if self.useAcx:
                if self.useAcy:
                    if self.useAcz:
                        self.pitch = self.get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
        if self.useRoll:
            if self.useAcx:
                if self.useAcy:
                    if self.useAcz: 
                        self.roll = self.get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)


    def getAcx(self):
        """Função retorna o valor de aceleração no eixo X
        :returns: Aceleração no eixo X
        """
        return self.acx
    
    def getAcy(self):
        """Função retorna o valor de aceleração no eixo Y
        :returns: Aceleração no eixo Y
        """
        return self.acy
    
    def getAcz(self):
        """Função retorna o valor de aceleração no eixo Z
        :returns: Aceleração no eixo Z
        """
        return self.acz
    
    def getGyx(self):
        """Função retorna o valor da taxa de giro no eixo X
        :returns: Taxa de giro no eixo X
        """
        return self.gyx
    
    def getGyy(self):
        """Função retorna o valor da taxa de giro no eixo Y
        :returns: Taxa de giro no eixo Y
        """
        return self.gyy
    
    def getGyz(self):
        """Função retorna o valor da taxa de giro no eixo Z
        :returns: Taxa de giro no eixo Z
        """
        return self.gyz
    
    def getPitch(self):
        """Função retorna o valor do pitch.
        :returns: Valor do Pitch atual
        """
        return self.pitch
    
    def getRoll(self):
        """Função retorna o valor do Roll.
        :returns: Valor do Roll atual
        """
        return self.roll
    
    def getTemp(self):
        """Função retorna o valor do temperatura.
        :returns: Valor do temperatura atual
        """
        return self.temp

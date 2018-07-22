class Celula(object):
    """Classe responsavel pela criaçao e comunicaçao de objetos
    do tipo Celula.
    Esta classe ira receber e tratar os dados de força vindos
    de cada uma das células (através do Arduino)."""

    def __init__(self, nome, apelido, cal_factor, arduino, UM = "N"):
        self.nome =  nome
        self.apelido = apelido
        self.calibration_factor = cal_factor
        self.arduino = arduino
        self.UM = UM
        self.force = 0

    def atualiza(self):
        dicioDeDados = self.arduino.getData()
        if self.apelido in dicioDeDados:
            raw_force = dicioDeDados[self.apelido]
            self.force = raw_force/self.calibration_factor

    def getForce(self):
        return self.force
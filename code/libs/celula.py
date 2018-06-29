class Celula(object):
    """Classe responsavel pela criaçao e comunicaçao de objetos
    do tipo Celula.
    Esta classe ira receber e tratar os dados de força vindos
    de cada uma das células (através do Arduino)."""

    def __init__(self, nome, apelido, arduino, UM = "N"):
        self.nome =  nome
        self.apelido = apelido
        self.arduino = arduino
        self.UM = UM
        self.force = 0

    def atualiza(self):
        dicioDeDados = self.arduino.getData()
        if self.apelido in dicioDeDados:
            self.force = dicioDeDados[self.apelido]

    def getForce(self):
        return self.force
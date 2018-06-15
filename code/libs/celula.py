class Celula(object):
    """Classe responsavel pela criaçao e comunicaçao de objetos
    do tipo Celula.
    Esta classe ira receber e tratar os dados de força vindos
    de cada uma das células (através do Arduino)."""

    def __init__(self, nome, apelido, UM = "Kg"):
        self.nome =  nome
        self.apelido = apelido
        self.UM = UM
        self.force = 0

    def updateForce(self, force):
        self.force = force

    def getForce(self):
        return self.force
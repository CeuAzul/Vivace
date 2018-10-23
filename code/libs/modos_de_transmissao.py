class SeletorDeModos(object):

    def __init__(self, criador):
        self.criador = criador

    def setModo(self, modo):
        """Função responsável por setar o modo de tranmissao de dados.
        """

        self.criador.modo.valor = modo
        print('Trocando para modo ' + str(modo) + ' de transmissao!')

        if modo == 1:
            # Do something
            pass
        elif modo == 2:
            # Do something
            pass
        else:
            # Do nothing
            pass
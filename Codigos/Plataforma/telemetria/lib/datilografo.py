#!/usr/bin/python
import os.path
from .dado import Dado

class Escritor:
    """É responsável pela escrita dos dados em um arquivo de texto.
    Esta classe será chamada toda vez que queremos gravar os valores
    que estão sendo adquirido pelos sensores em um arquivo de texto.

    A classe pode ser modificada das seguintes maneiras:
    - Indicar o tipo de separador dos dados (virgula, espaço, tabulação etc..)
    - Se deve colocar o nome dos dados na primeira linha.
    - Se deve colocar a unidade de medida na segunda linha
    - Nome do arquivo
    - Extensão do arquivo

    Para utilizar a classe seguimos os seguintes passos:
    1- Inicializamos a classe configurando o escritor para criar o arquivo do jeito que quisermo.
    2- Chamamos a função setDado com um vetor de objetos criados da classe "Dado", já com nome e unidade de medida.
    3- Quando quisermos que a gravação de dados inicie, devemos chamar "fazCabecalho()"
    4- Cada vez que quiser que o Escritor grave uma linha dado, primeiro atualize o vetor de dados "setDados()" e depois invoque "escreveLinhaDado(self)"
    5- Veja o dado sendo gravado e corra para o abraço!

    Multiplos inicializações são criadas arquivos com o mesmo nome, mas com número diferente ex:
    Nome arquivo - 01
    Nome arquivo - 02
    Nome arquivo - 03
    ...
    """
    def __init__(self, separador=",", printaNome=True, printaUM=True, nomeArquivo="Telemetria - ", extensao=".csv"):
        """Construtor inicializa parâmetros de configuração do Escritor
        No construtor ele já cria o arquivo, verifica se nome já existe, caso já exista, adiciona 1 no nome.

        :param separador: Especifica o tipo de separados dos valores mais comum é virgula espaço ou tabulação
        :param printaNome: Indicador se deve ser gravado o nome do dado na primeira linha do cabeçalho
        :param printaUM: Indicador se deve ser gravado a unidade de medida na segunda linha do cabeçalho
        :param nomeArquivo: Nome do arquivo
        :param extensao: Extensão do arquivo a ser criado
        """

        self.dados = []                 #vetor de Dado()
        self.separador = separador
        self.printaNome = printaNome
        self.printaUM = printaUM
        self.nomeArquivo = nomeArquivo
        self.extensao = extensao
        self.numeroArquivo = 1
        while os.path.exists(self.nomeArquivo+str(self.numeroArquivo)+self.extensao):
            self.numeroArquivo += 1
        self.nomeCompleto = self.nomeArquivo+str(self.numeroArquivo)+self.extensao
        
    def addDado(self, d):
        """Função que adiciona um dado no vetor de dados.
        NÃO UTILIZAR ESSA FUNÇÃO A MENOS QUE VOCÊ SAIBA O QUE TA FAZENDO.
        :param d: Dado a ser adicionado.
        """
        self.dados.append(d)

    def setDados(self, d):
        """Função que atualiza o vetor de dados do Escritor com os dados que vem como parâmetro dessa função.
        O Escritor apenas consegue ver os dados que foram passados por meio dessa função.
        É utilizada como a porta de entrada para os dados que serão escritos.
        
        :param d: Vetor de Dado que será escrito na ordem do vetor.
        """
        self.dados = d

    def fazCabecalho(self):
        """Função que escreve o cabeçalho do arquivo:
        Primeira linha (se printaNome=True) = Printa o nome dos dados
        Segunda linha (se printaUM=True) = Printa unidade de medida na segunda linha
        """
        file = open(self.nomeCompleto, "a")
        if self.printaNome:
            for x in self.dados:
                if x.gravaDado:
                    file.write("%s%s" % (x.nome, self.separador))
        file.write("\n")
        if self.printaUM:
            for x in self.dados:
                if x.gravaDado:
                    file.write("%s%s" % (x.unidadeMedida, self.separador))
        file.write("\n")

    def escreveLinhaDado(self):
        """Função que escreve a linha com os valores atuais do dado separado pelo separador.
           Antes de gravar, a função verifica se o dado é mesmo para ser gravado ou não.
        """
        file = open(self.nomeCompleto, "a")
        for x in self.dados:
            if x.gravaDado:
                file.write("%s%s" % (x.valor, self.separador))
        file.write("\n")            



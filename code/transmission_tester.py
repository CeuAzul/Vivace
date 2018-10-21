from libs.telepatia import Transmissor
from thredeiro import Thredeiro
from datetime import datetime
import time
import math


initialTime = datetime.now()
timeNow = 0

index = 0
sinIndex = 0

def atualizar_valores(delay):
    global index
    global sinIndex
    global timeNow

    while True:
        start_time = time.time()
        index += 1
        if index >= 360:
            index = 0

        sinIndex = math.sin(math.radians(index))

        now = datetime.now()
        timeNow = (now - initialTime).total_seconds()
        print('Time to calculate: ' + str(time.time() - start_time))

        time.sleep(delay)

def enviar_pacotes(delay):
    print('Transmitindo')
    while True:
        print('\033[H\033[J')
        start_time = time.time()
        transmissor.transmiteDadoProtocolado("htb", 1)
        transmissor.transmiteDadoProtocolado("tmt", 1)
        transmissor.transmiteDadoProtocolado("gvd", 1)
        transmissor.transmiteDadoProtocolado("cfg", 1)
        transmissor.transmiteDadoProtocolado("id1", index)
        transmissor.transmiteDadoProtocolado("si1", sinIndex)
        transmissor.transmiteDadoProtocolado("tm1", timeNow)
        print('Time to transmit: ' + str(time.time() - start_time))
        time.sleep(delay)

transmissor = Transmissor(",", True, 57600, 'UTF-8')

threadAtualizacao = Thredeiro('Thread de atualizacao de dados', atualizar_valores, 0.02)
threadEnvio = Thredeiro('Thread de envio de pacotes', enviar_pacotes, 0.05)
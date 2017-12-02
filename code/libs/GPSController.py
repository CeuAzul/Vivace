#!/usr/bin/python
# -*- coding: utf-8 -*-

from .gps.gps import *
import time
import threading
import math


class GpsController(threading.Thread):
    """Classe responsavel pela comunicaçao com a biblioteca GPS.
    """

    def __init__(self):
        """Cria o objeto GpsController em uma Thread separada.
        """

        threading.Thread.__init__(self)
        self.gpsd = GPS(mode=WATCH_ENABLE)  # starting the stream of info
        self.running = False

    def run(self):
        """Inicia o recebimento de dados do GPS.
        """
        self.running = True
        while self.running:
            # grab EACH set of gpsd info to clear the buffer
            try:
                self.gpsd.next()
            except:
                pass

    def stopController(self):
        """Corta o recebimento de dados do GPS.
        """
        self.running = False

    @property
    def fix(self):
        """Retorna o valor de indicaçao de Fix.

        :returns: Valor de Fix
        """
        return self.gpsd.fix

    @property
    def utc(self):
        """Retorna a posiçao em UTC.

        :returns: Posiçao em UTC
        """
        return self.gpsd.utc

    @property
    def satellites(self):
        """Retorna o numero de satelites visiveis.

        :returns: Numero de satelites visiveis
        """
        return self.gpsd.satellites


if __name__ == '__main__':
    # create the controller
    gpsc = GpsController()
    try:
        # start controller
        gpsc.start()
        while True:
            print("latitude ", gpsc.fix.latitude)
            print("longitude ", gpsc.fix.longitude)
            print("time utc ", gpsc.utc, " + ", gpsc.fix.time)
            print("altitude (m)", gpsc.fix.altitude)
            print("eps ", gpsc.fix.eps)
            print("epx ", gpsc.fix.epx)
            print("epv ", gpsc.fix.epv)
            print("ept ", gpsc.gpsd.fix.ept)
            print("speed (m/s) ", gpsc.fix.speed)
            print("climb ", gpsc.fix.climb)
            print("track ", gpsc.fix.track)
            print("mode ", gpsc.fix.mode)
            print("sats ", gpsc.satellites)
            time.sleep(0.5)

    # Ctrl C
    except KeyboardInterrupt:
        print("User cancelled")

    # Error
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
    finally:
        print("Stopping gps controller")
        gpsc.stopController()
        # wait for the tread to finish
        gpsc.join()

    print("Done")

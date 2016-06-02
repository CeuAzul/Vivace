from gps import *
import time
import threading
import math

class GpsController(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.gpsd = gps.GPS(mode=WATCH_ENABLE) #starting the stream of info
        self.running = False
    
    def run(self):
        self.running = True
        while self.running:
            # grab EACH set of gpsd info to clear the buffer
            self.gpsd.next()

    def stopController(self):
        self.running = False
  
    @property
    def fix(self):
        return self.gpsd.fix

    @property
    def utc(self):
        return self.gpsd.utc

    @property
    def satellites(self):
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

    #Ctrl C
    except KeyboardInterrupt:
        print("User cancelled")
        
    #Error
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
    finally:
        print("Stopping gps controller")
        gpsc.stopController()
        #wait for the tread to finish
        gpsc.join()
      
    print("Done")

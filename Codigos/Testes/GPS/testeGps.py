from GPSController import GpsController
#create controller
gpsc = GpsController()

#start controller
gpsc.start()
while(True):
    #read latitude and longitude
    print(gpsc.fix.latitude)
    print(gpsc.fix.longitude)
    

#stop controller
gpsc.stopController()

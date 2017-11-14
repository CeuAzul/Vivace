import os
import datetime
import shutil
from shutil import copytree, ignore_patterns

nomesPastas = os.listdir("/media/pi")

try:
    for pen in nomesPastas:
        if pen != "SETTINGS" :
            d = datetime.datetime.now().strftime('%d_%m_%Y__%H_%M_%S%f')[:-3]
            source = '/home/pi/Telemetria/Codigos/Plataforma/telemetria/Dados'
            destination = '/media/pi/%s/Telemetria/Dados_%s' % (pen,d)
            copytree(source, destination)
except Exception as e:
    print(e)

from hcsr04sensor import sensor
import datetime

def main():
    '''Example script using hcsr04sensor module for Raspberry Pi'''
    trig_pin = 23
    echo_pin = 24
    # Default values
    # unit = 'metric'
    # temperature = 20
    # round_to = 1
    tempoAntesFuncao = datetime.datetime.now()

    #  Create a distance reading with the hcsr04 sensor module
    value = sensor.Measurement(trig_pin, echo_pin)
    raw_measurement = value.raw_distance()

    # To overide default values you can pass the following to value
    # value = sensor.Measurement(trig_pin,
    #                            echo_pin,
    #                            temperature=10,
    #                            round_to=2
    #                            )


    # Calculate the distance in centimeters
    metric_distance = value.distance_metric(raw_measurement)
    tempoDepoisFuncao = datetime.datetime.now()
    tempoFuncao = tempoDepoisFuncao - tempoAntesFuncao
    print("The Distance = {} centimeters".format(metric_distance), ", tempo: ",tempoFuncao.microseconds)

if __name__ == "__main__":
    main()

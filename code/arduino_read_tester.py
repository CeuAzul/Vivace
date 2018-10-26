import serial
import serial.tools.list_ports as prtlst

def connect():
    print("########## Trying Arduino! ##########")
    pts = prtlst.comports()
    for pt in pts:
        if 'USB' or 'ACM' in pt[0]:
            if 'USB2.0' in pt[1]:
                porta = pt[0]
                devName = pt[1]
                print('Connecting on Arduino ' + devName + ' on port ' + porta)
                serialo = serial.Serial(port=porta, baudrate=115200, timeout=0.01)
                return serialo

def updateData(serial):
    try:
        if serial.in_waiting > 0:
            linha_de_dados = serial.readline().decode('utf-8')
            print(linha_de_dados)

            if(linha_de_dados != ""):
                linha_de_dados = linha_de_dados.replace("\r\n", "")
                if linha_de_dados.startswith("!") and linha_de_dados.endswith("@"):
                    linha_de_dados = linha_de_dados.replace(" ", "")
                    linha_de_dados = linha_de_dados.replace("!", "")
                    linha_de_dados = linha_de_dados.replace("@", "")
                    dados = linha_de_dados.split(";")
                    receivedChecksum = 0
                    calculatedChecksum = 0
                    tempDicioDeDados = {}
                    for dado in dados:
                        try:
                            apelido, valor = dado.split("=")
                            if apelido == 'gyz':
                                print(valor)
                            if apelido != 'cks':
                                calculatedChecksum += float(valor)
                                tempDicioDeDados[apelido] = float(valor)
                            else:
                                receivedChecksum = valor
                        except:
                            pass

                        # if abs(float(receivedChecksum) - float(calculatedChecksum)) <=1:
                        #   dicioDeDados.update(tempDicioDeDados)
    except:
        pass

def main():
    print('Initializing')
    serialo = connect()
    while True:
        updateData(serialo)

if __name__ == '__main__':
    main()
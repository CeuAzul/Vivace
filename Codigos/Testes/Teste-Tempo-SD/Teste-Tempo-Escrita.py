#!/usr/bin/python
import datetime

print("Bytes, Tempo de abertura arquivo, Tempo escrita no buffer, Tempo fechar arquivo, Tempo print, Tempo função")
depoisPrint = datetime.datetime.now()
antesPrint = datetime.datetime.now()
depoisFuncao = datetime.datetime.now()
for x in range(0, 2048):
    antesFuncao = datetime.datetime.now()
    antesAbrir = datetime.datetime.now()
    file = open("Teste.txt", "a")
    depoisAbrir = datetime.datetime.now()
    
    a = ''
    for y in range(0, (x+1)):
        a = a+'A'
        
    antesEscrita = datetime.datetime.now()
    file.write("%s\n" % (a))
    depoisEscrita = datetime.datetime.now()

    antesFechar = datetime.datetime.now()
    file.close()
    depoisFechar = datetime.datetime.now()

    
    tempoAbrir = depoisAbrir - antesAbrir
    tempoEscrita = depoisEscrita - antesEscrita
    tempoClose = depoisFechar - antesFechar
    tempoPrint = depoisPrint - antesPrint
    tempoFuncao = depoisFuncao - antesFuncao
    
    antesPrint = datetime.datetime.now()
    print("%d, %d, %d, %d, %d, %d" % ((x+1), tempoAbrir.microseconds, tempoEscrita.microseconds, tempoClose.microseconds, tempoPrint.microseconds, tempoFuncao.microseconds))
    depoisPrint = datetime.datetime.now()

    depoisFuncao = datetime.datetime.now()


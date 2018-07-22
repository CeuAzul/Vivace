#!/usr/bin/python
# -*- coding: utf-8 -*

class SondaAoA:
    def __init__(self, nome, apelido, c1, c2, ap_pt_dif, ap_pt_dyn, pitots, UM = 'deg'):
        self.nome = nome
        self.apelido = apelido
        self.c1 = c1
        self.c2 = c2
        self.apelido_pitot_dif = ap_pt_dif
        self.apelido_pitot_dyn = ap_pt_dyn
        self.pitots = pitots
        self.UM = UM

        self.difPressure = 0
        self.dynPressure = 0
        self.aoa = 0

        self.ultimosCemDifPressure = [0] * 100
        self.ultimosCemDynPressure = [0] * 100

    def atualiza(self, samples=10):
        for pitot in self.pitots:
            if pitot.apelido == self.apelido_pitot_dif:
                self.difPressure = pitot.getPressaoDinRef()
                self.ultimosCemDifPressure.pop(0)
                self.ultimosCemDifPressure.append(self.difPressure)
            if pitot.apelido == self.apelido_pitot_dyn:
                self.dynPressure = pitot.getPressaoDinRef()
                self.ultimosCemDynPressure.pop(0)
                self.ultimosCemDynPressure.append(self.dynPressure)

        avgDifPress = sum(self.ultimosCemDifPressure[-samples:]) / samples
        avgDynPress = sum(self.ultimosCemDynPressure[-samples:]) / samples

        try:
            self.aoa = (self.c1 * avgDifPress) / (avgDynPress ** self.c2)
        except:
            self.aoa = 'OutOfRange'

        if self.aoa is not 'OutOfRange':
            if isinstance(self.aoa, complex):
                self.aoa = 'OutOfRange'
            elif self.aoa>1000.0 or self.aoa<1000.0:
                self.aoa = 'OutOfRange'

    def getDifPressure(self):
        return self.difPressure

    def getDynPressure(self):
        return self.dynPressure

    def getAoA(self):
        return self.aoa


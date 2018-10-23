#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading

class Thredeiro (threading.Thread):

    def __init__(self, name, funcaoAlvo, delay):
        threading.Thread.__init__(self, target=funcaoAlvo, args=(delay,))
        print('Thread de ' + name + ' iniciada')
        self.start()

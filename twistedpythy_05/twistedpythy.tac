# -*- coding: koi8-r -*-
# twistedpythy.tac:  simple TAC for TwistedPythy
# Pythy <the.pythy@gmail.com>

from twisted.application import service

from TwistedPythy import tap

options = {
    'listen-port': 3000,    # порт, на котором ждать соединений
    'delay': 5,             # задержка перед ответом
    'encoding': 'utf-8',    # кодировка транспорта
    }


application = service.Application("TwistedPythy")
s = tap.makeService(options)
s.setServiceParent(application)

# coding=utf-8
#
# Created by junn, on 2019-09-01
#

# Warm up

import logging

logs = logging.getLogger(__name__)


class Dog:

    def __init__(self, name):
        self.name = name
        self.position = 0
        self.meat = None
        print("Dog %s is created" % name)

    def run_step(self):
        self.position += 1

    def eat(self, meat):
        self.meat = meat
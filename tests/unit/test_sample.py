# coding=utf-8
#
# Created by junn, on 2019-09-01
#

import logging
from unittest import TestCase

from kata.sample import Dog

logs = logging.getLogger(__name__)


def inc(x):
    return x + 1


def test_inc():
    assert inc(3) == 4


def test_fail():
    assert (1, 2) == (1, 2)


class TestMyClass(object):
    def test_one(self):
        x = "hello"
        assert 'e' in x

    def test_two(self):
        x = "world"
        assert hasattr(x, 'join')


class TestDog(TestCase):

    def setUp(self):
        self.dog = Dog('default')

    def test_eat(self):
        self.dog.name = 'kitty'
        assert self.dog.meat is None

        meat = 'pig'
        self.dog.eat(meat)
        assert self.dog.meat == meat

    def test_run_step(self):
        position = self.dog.position
        self.dog.run_step()
        assert self.dog.position == position + 1


# coding=utf-8
#
# Created by junn, on 2019-09-24
#

from unittest import TestCase

from kata.marsrover import MarsRover, DIRECTION


def assert_rover_equal(rover, x, y, direction):
    assert rover.x == x
    assert rover.y == y
    assert rover.direction == direction


class MarsRoverTest(TestCase):

    # def setUp(self):
    #     self.rover = MarsRover(0, 0, DIRECTION.E)

    def test_init_marsrover(self):
        rover = MarsRover(8, 12, DIRECTION.N)
        assert_rover_equal(rover, 8, 12, DIRECTION.N)

    def test_rover_forward(self):
        rover = MarsRover(8, 12, DIRECTION.N)
        rover.forward()
        assert_rover_equal(rover, 8, 13, DIRECTION.N)

        rover = MarsRover(8, 12, DIRECTION.S)
        rover.forward()
        assert_rover_equal(rover, 8, 11, DIRECTION.S)

        rover = MarsRover(8, 12, DIRECTION.W)
        rover.forward()
        assert_rover_equal(rover, 7, 12, DIRECTION.W)

        rover = MarsRover(8, 12, DIRECTION.E)
        rover.forward()
        assert_rover_equal(rover, 9, 12, DIRECTION.E)

    def test_rover_receive_border(self):
        rover = MarsRover(8, 12, DIRECTION.N)
        rover.receive_district_info(100, 100)
        assert rover.border_len == 100
        assert rover.border_wid == 100

    def test_rover_cross_border(self):
        rover = MarsRover(0, 0, DIRECTION.W)
        rover.forward()
        assert_rover_equal(rover, 0, 0, DIRECTION.W)

        rover.direction = DIRECTION.S
        rover.forward()
        assert_rover_equal(rover, 0, 0, DIRECTION.S)

    def test_rover_turn_direction(self):
        rover = MarsRover(10, 10, DIRECTION.E)
        rover.turn_left()
        rover.forward()
        assert_rover_equal(rover, 10, 11, DIRECTION.N)

# coding=utf-8
#
# Created by junn, on 2019-10-25
#

import pytest
from unittest import TestCase

from kata.bowling import (
    Bowling, FrameFactory,
    Frame, StrikeFrame, SpareFrame, LastFrame
)


class BowlingTotalPointsTest(TestCase):

    def test_all_normal_frames_total_points(self):
        sequence = "9- 9- 9- 9- 9- 9- 9- 9- 9- 9-"
        b = Bowling(sequence)
        assert b.get_total_points() == 90

    def test_all_strike_frames_total_points(self):
        sequence = "x x x x x x x x x xxx"
        b = Bowling(sequence)
        assert b.get_total_points() == 300

    def test_normal_strike_frames_total_points(self):
        sequence = "9- x 9- 9- 9- 9- 9- 9- 9- 9-"
        b = Bowling(sequence)
        assert b.get_total_points() == 100

    def test_all_spare_frames_total_points(self):
        sequence = "5/ 5/ 5/ 5/ 5/ 5/ 5/ 5/ 5/ 5/5"
        b = Bowling(sequence)
        assert b.get_total_points() == 150

    def test_bowling_total_points(self):
        sequence = "9- x 3/ 5- 5- 5- 5- 5- 5- 5/x"
        b = Bowling(sequence)
        assert b.get_total_points() == 94

        sequence = "9- x 3/ 5- 5- 5- 5- 5- 5- xxx"
        b = Bowling(sequence)
        assert b.get_total_points() == 104

        sequence = "9- x 3/ 5- 5- 5- 5- 5- 5- -/1"
        b = Bowling(sequence)
        assert b.get_total_points() == 85


class FrameFactoryTest(TestCase):

    def test_frame_factory(self):
        sequence = "9- x 9- 9- 9- 9- 9- 9- 9- 9-"
        frames = FrameFactory.create_frames(sequence)
        assert isinstance(frames[0], Frame)
        assert isinstance(frames[1], StrikeFrame)

    def test_frame_factory_with_complex_frames(self):
        sequence = "9- x 3/ 9- 9- 9- 9- 9- 9- xxx"
        frames = FrameFactory.create_frames(sequence)
        assert isinstance(frames[2], SpareFrame)
        assert isinstance(frames[9], LastFrame)
        assert not isinstance(frames[1], LastFrame)


class SingleFramePointsTest(TestCase):

    def test_frame_points(self):
        sequence = "9- x 9- 9- 9- 9- 9- 9- 9- 9-"
        frames = FrameFactory.create_frames(sequence)
        assert frames[0].get_points() == 9
        assert frames[1].get_points() == 19
        assert frames[9].get_points() == 9

        assert frames[0].next == frames[1]
        assert frames[0].next.get_first_roll_pins() == 10

    def test_spare_frame_points(self):
        sequence = "9- x -/ 9/ 9- 9- 9- 9- 9- -/x"
        frames = FrameFactory.create_frames(sequence)
        assert frames[1].get_points() == 20
        assert frames[2].get_points() == 19
        assert frames[2].get_points() == 19
        assert frames[9].get_points() == 20

        assert frames[9].next is None

    def test_spare_and_strike_frame_points(self):
        sequence = "9- x -/ 9/ 9- -- 9- 9- 9- 9/1"
        frames = FrameFactory.create_frames(sequence)
        assert frames[2].get_points() == 19
        assert frames[9].get_points() == 11

        assert frames[5].get_points() == 0
        assert frames[5].get_first_roll_pins() == 0
        assert frames[5].get_total_rolls_pins() == 0


class FrameRollPinsTest(TestCase):

    def test_normal_frame_pins(self):
        frame = Frame("9-")
        assert frame.has_two_rolls()
        assert frame.get_first_roll_pins() == 9
        assert frame.get_total_rolls_pins() == 9

        frame = Frame("35")
        assert frame.has_two_rolls()
        assert frame.get_first_roll_pins() == 3
        assert frame.get_total_rolls_pins() == 8

    def test_strike_frame_pins(self):
        frame = StrikeFrame('x')
        assert not frame.has_two_rolls()
        assert frame.get_first_roll_pins() == 10
        assert frame.get_total_rolls_pins() == 10

    def test_spare_frame_pins(self):
        frame = SpareFrame('9/')
        assert frame.has_two_rolls()
        assert not frame.has_three_rolls()
        assert frame.get_first_roll_pins() == 9
        assert frame.get_total_rolls_pins() == 10

    def test_last_frame_pins(self):
        frame = LastFrame('3-')
        assert frame.has_two_rolls()
        assert not frame.has_three_rolls()
        assert frame.get_first_roll_pins() == 3
        assert frame.get_total_rolls_pins() == 3

        frame = LastFrame('9/x')
        assert frame.has_three_rolls()
        assert frame.get_first_roll_pins() == 9
        assert frame.get_total_rolls_pins() == 20

        frame = LastFrame('9/5')
        assert frame.has_three_rolls()
        assert frame.get_total_rolls_pins() == 15

        frame = LastFrame('xxx')
        assert not frame.has_two_rolls()
        assert frame.get_first_roll_pins() == 10
        assert frame.get_total_rolls_pins() == 30

        frame = LastFrame('-/-')
        assert frame.has_three_rolls()
        assert frame.get_first_roll_pins() == 0
        assert frame.get_total_rolls_pins() == 10

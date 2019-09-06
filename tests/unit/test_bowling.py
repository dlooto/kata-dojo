# coding=utf-8
#
# Created by junn, on 2019-09-06
#

from unittest import TestCase

from kata.bowling import (
    BowlingScorer, Frame, StrikeFrame, SpareFrame, LastFrame, FrameFactory
)


class BowlingTest(TestCase):
    """
    “x” 表示一个strike, “/” 表示一个 spare, “-” 代表未投中
    """

    def setUp(self) -> None:
        self.bs = BowlingScorer()

    # def test_new_bowling_scoring(self):
    #     self.bs.sequence = '9-9-9-9-9-9-9-9-9-9-'
    #     assert self.bs.total_points() == 90


def test_one_frame_score():
    frame = Frame(1, '9-')
    assert frame.get_first_roll_pins() == 9
    assert frame.get_total_rolls_pins() == 9

    frame = StrikeFrame(1, 'x')
    assert frame.get_first_roll_pins() == 10
    assert frame.get_total_rolls_pins() == 10

    frame = SpareFrame(1, '9/')
    assert frame.get_first_roll_pins() == 9
    assert frame.get_total_rolls_pins() == 10

    frame = LastFrame(9, '9/x')
    assert frame.get_first_roll_pins() == 9
    assert frame.get_total_rolls_pins() == 10

    frame = Frame(1, '35')
    assert frame.get_first_roll_pins() == 3
    assert frame.get_total_rolls_pins() == 8

def test_frame_factory():
    sequence = '9- x 3/ 5- 5- 5- 5- 5- 5- 8-'
    frames = FrameFactory.create_frames(sequence)

    assert isinstance(frames[0], Frame)
    assert isinstance(frames[1], StrikeFrame)
    assert isinstance(frames[2], SpareFrame)
    assert isinstance(frames[9], LastFrame)

    assert frames[2].index == 2
    assert frames[2].next.get_first_roll_pins() == 5

def test_create_frames_exception():
    pass

def test_strike_frame_create():
    sequence = 'x x x x x x x x x x x x'
    bs = BowlingScorer(sequence)
    assert len(bs.frames) == 10
    assert bs.total_points() == 300

def test_total_points():
    sequence = '9- 9- 9- 9- 9- 9- 9- 9- 9- 9-'
    bs = BowlingScorer(sequence)
    assert bs.total_points() == 90

    sequence = '5/ 5/ 5/ 5/ 5/ 5/ 5/ 5/ 5/ 5/5'
    bs = BowlingScorer(sequence)
    assert bs.total_points() == 150


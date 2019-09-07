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

    # def setUp(self) -> None:
    #     self.bs = BowlingScorer()

    def test_frames_length_less_than_10_exception(self):
        sequence = '9- x 3/ 5- 5- 5- 5- 5- 5- '
        # self.assertRaises(Exception, FrameFactory.create_frames, sequence)
        self.assertRaisesRegex(Exception, 'Frame length less than 10 *',
                               FrameFactory.create_frames, sequence)

    def test_frames_create_sequence_exception(self):
        sequence = '9- x 3/ 5- 5- 5u 5- 5- 5- 5-'
        self.assertRaisesRegex(Exception, 'invalid literal for int() *',
                               FrameFactory.create_frames, sequence)


def test_frame_points():
    sequence = '9- x 3/ 5- 5- 5- 5- 5- 5- x x x'
    frames = FrameFactory.create_frames(sequence)

    assert frames[0].get_points() == 9
    assert frames[1].get_points() == 20
    assert frames[2].get_points() == 15

    assert not frames[1].has_two_rolls()
    assert not frames[2].has_three_rolls()
    assert frames[3].has_two_rolls()
    assert frames[9].has_three_rolls()


def test_one_frame_pins():
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


def test_strike_frame_create():
    sequence = 'x x x x x x x x x x x x'
    bs = BowlingScorer(sequence)
    assert len(bs.frames) == 10
    assert bs.total_points() == 300

    sequence = '3- 3- 3- 3- 3- 3- 3- 3/ x x x x'
    bs = BowlingScorer(sequence)
    assert len(bs.frames) == 10
    assert bs.total_points() == 101


def test_normal_frame_total_points():
    sequence = '9- 9- 9- 9- 9- 9- 9- 9- 9- 9-'
    bs = BowlingScorer(sequence)
    assert bs.total_points() == 90

    sequence = '9- 9- 9- 9- 9- 9- 9- 9- 9- 9/x'
    bs = BowlingScorer(sequence)
    assert bs.total_points() == 101


def test_all_spare_frame_total_points():
    sequence = '5/ 5/ 5/ 5/ 5/ 5/ 5/ 5/ 5/ 5/5'
    bs = BowlingScorer(sequence)
    assert bs.total_points() == 150





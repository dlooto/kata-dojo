# coding=utf-8
#
# Created by junn, on 2019-10-25
#


class Bowling:

    def __init__(self, sequence):
        self.frames = FrameFactory.create_frames(sequence)

    def get_total_points(self):
        total_points = 0
        for frame in self.frames:
            total_points += frame.get_points()
        return total_points


class FrameFactory:

    @classmethod
    def create_frames(cls, sequence):
        frame_str_list = sequence.split(' ')

        result_frames = []
        for i in range(len(frame_str_list) - 1):
            if 'x' in frame_str_list[i]:
                result_frames.append(StrikeFrame(frame_str_list[i]))
            elif '/' in frame_str_list[i]:
                result_frames.append(SpareFrame(frame_str_list[i]))
            else:
                result_frames.append(Frame(frame_str_list[i]))

        result_frames.append(LastFrame(frame_str_list[9]))

        for i in range(len(result_frames)):
            if i >= 9:
                break
            result_frames[i].next = result_frames[i+1]

        return result_frames


class Frame:

    def __init__(self, frame_str, next_frame=None):
        self.rolls = self._init_rolls(frame_str)
        self.next = next_frame

    def _init_rolls(self, frame_str):
        return [
            Roll(to_int(frame_str[0])),
            Roll(0) if frame_str[1] == '-' else Roll(to_int(frame_str[1]))
        ]

    def has_two_rolls(self):
        return True

    def has_three_rolls(self):
        return False

    def get_first_roll_pins(self):
        return self.rolls[0].pins

    def get_second_roll_pins(self):
        return self.rolls[1].pins

    def get_total_rolls_pins(self):
        # return self.get_first_roll_pins() + self.get_second_roll_pins()
        sum_pins = 0
        for roll in self.rolls:
            sum_pins += roll.pins
        return sum_pins

    def get_points(self):
        sum_points = 0
        for roll in self.rolls:
            sum_points += roll.pins
        return sum_points


class StrikeFrame(Frame):

    def _init_rolls(self, frame_str):
        return [Roll(10)]

    def has_two_rolls(self):
        return False

    def get_second_roll_pins(self):
        raise Exception("No the second roll")

    def get_total_rolls_pins(self):
        return self.get_first_roll_pins()

    def get_points(self):
        if self.next.has_two_rolls() or self.next.has_three_rolls():
            return 10 + self.next.get_first_roll_pins() + self.next.get_second_roll_pins()

        return 10 + self.next.get_first_roll_pins() + self.next.next.get_first_roll_pins()


class SpareFrame(Frame):

    def _init_rolls(self, frame_str):       # 9/ 9/  -/ -/
        pins = to_int(frame_str[0])
        return [Roll(pins), Roll(10 - pins)]

    def get_total_rolls_pins(self):
        return 10

    def get_points(self):
        return 10 + self.next.get_first_roll_pins()


class LastFrame(Frame):

    def _init_rolls(self, frame_str):   # x12 xxx -/x -/9 9/1 35
        if '/' in frame_str:
            first_pins = to_int(frame_str[0])
            return [Roll(first_pins), Roll(10-first_pins), Roll(to_int(frame_str[2]))]

        return [Roll(to_int(s)) for s in frame_str]

    def has_two_rolls(self):
        return len(self.rolls) == 2

    def has_three_rolls(self):
        return len(self.rolls) == 3


class Roll:

    def __init__(self, pins):
        self.pins = pins


def to_int(s):
    if s == '-':
        return 0
    elif s == 'x':
        return 10
    else:
        return int(s)


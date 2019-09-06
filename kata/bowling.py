# coding=utf-8
#
# Created by junn, on 2019-09-06
#


class FrameFactory:

    @classmethod
    def create_frames(cls, sequence):
        """
        :param sequence: 以空格分隔的字符串，如'9- x 3/ 5- 5- 5- 5- 5- 5- 8-'
        :return:
        """

        # Build Frame list
        frames = sequence.split(' ')
        if len(frames) < 10:
            raise Exception("Frame length less than 10 ")

        results = []
        for i in range(10-1):
            if 'x' in frames[i]:
                results.append(StrikeFrame(i, frames[i]))
            elif '/' in frames[i]:
                results.append(SpareFrame(i, frames[i]))
            else:
                results.append(Frame(i, frames[i]))  # '8-' or '33'

        if len(frames) > 10:
            results.append(LastFrame(9, ''.join([s for s in frames[9:]])))
        else:
            results.append(LastFrame(9, frames[9]))

        # Add next pointer
        for i in range(len(results)):
            if i < 9:
                results[i].next = results[i+1]

        return results


class BowlingScorer:
    """
    保龄计分
    """

    def __init__(self, sequence):
        self.frames = FrameFactory.create_frames(sequence)

    def total_points(self):
        sums = 0
        for frame in self.frames:
            sums += frame.get_points()

        return sums


class Frame:
    """
    某一轮投球。两次投掷，未能击倒所有瓶子的情况
    """

    def __init__(self, index, rolls_str, next_frame=None):
        self.index = index          # 轮次序号
        self.rolls = self._init_rolls(rolls_str)      # 1-2次投掷
        self.next = next_frame

    def _init_rolls(self, rolls_str):
        i = 0
        rolls = []
        for s in rolls_str:
            if s == '-':
                rolls.append(Roll(i, 0))
            else:
                rolls.append(Roll(i, int(s)))
            i += 1
        return rolls

    def get_points(self):
        sum_pins = 0
        for roll in self.rolls:
            sum_pins += roll.pins
        return sum_pins

    def has_two_rolls(self):
        """是否有2次投掷"""
        return True

    def has_three_rolls(self):
        return False

    def get_first_roll_pins(self):
        """首次投掷击倒的瓶子数"""
        return (self.rolls[0]).pins

    def get_total_rolls_pins(self):
        """两次投掷击倒的瓶子总数"""
        return (self.rolls[0]).pins + (self.rolls[1]).pins


class StrikeFrame(Frame):
    """ 一投全中，则只投掷一次 """

    def _init_rolls(self, rolls_str):
        return [Roll(0, 10)]

    def get_points(self):
        if self.next.has_two_rolls() or self.next.has_three_rolls():
            return 10 + self.next.get_total_rolls_pins()

        # 单次
        return 10 + self.next.get_first_roll_pins() + self.next.next.get_first_roll_pins()

    def has_two_rolls(self):
        """ 是否仅投掷了一次 """
        return False

    def get_total_rolls_pins(self):
        return self.get_first_roll_pins()


class SpareFrame(Frame):
    """ 二投中，本轮将投2次 """

    def _init_rolls(self, rolls_str):
        pins = int(rolls_str[0])
        return [Roll(0, pins), Roll(1, 10-pins)]

    def get_points(self):
        return 10 + (self.next.rolls[0]).pins

    def get_total_rolls_pins(self):
        return 10


class LastFrame(Frame):
    """ 最后一轮. 可能有3次投掷(Strike/Spare时)，或者2次投掷 """

    def _init_rolls(self, rolls_str):
        if '/' in rolls_str:
            first_pins = to_int(rolls_str[0])
            return [Roll(0, first_pins), Roll(1, 10-first_pins), Roll(2, to_int(rolls_str[2]))]

        rolls = []
        for i in range(len(rolls_str)):
            rolls.append(Roll(i, to_int(rolls_str[i])))

        return rolls

    def has_three_rolls(self):
        """最后一轮是否有次投掷（即第一次投掷为全中）"""
        return len(self.rolls) == 3


def to_int(roll_str):
    """ roll_str == '/'需要单独计算  """
    if roll_str == 'x':
        return 10
    elif roll_str == '-':
        return 0
    return int(roll_str)


class Roll:
    """ 一次投掷 """

    # {"x": 10, "/": , "-": 0}

    def __init__(self, index, pins):
        """

        :param index: 在一轮投掷中的第几次投掷
        :param pins: 投掷击倒的瓶子数
        :param next_roll: 同一frame中的下一次投掷，frame中最后一次投掷next=None
        """
        self.index = index
        self.pins = pins


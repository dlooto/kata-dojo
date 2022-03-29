# coding=utf-8
#
# Created by junn, on 2019-09-24
#


class DIRECTION:
    N = 'N'
    S = 'S'
    E = 'E'
    W = 'W'


class MarsRover:
    """
    以(0, 0)为坐标原点、N/S方向为Y轴、W/E方向为X轴建立二维坐标系
    """

    border_len = 100
    border_wid = 100

    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction

    def forward(self):
        if self.direction == DIRECTION.N:
            self.y += 1
        elif self.direction == DIRECTION.S:
            self.y -= 1
        elif self.direction == DIRECTION.W:
            self.x -= 1
        else:
            self.x += 1

        self.correct_xy()

    def correct_xy(self):
        if self.x < 0:
            self.x = 0
        elif self.x > self.border_len:
            self.x = self.border_len
        if self.y < 0:
            self.y = 0
        if self.y > self.border_wid:
            self.y = self.border_wid

    def turn_left(self):
        pass

    def turn_right(self):
        pass

    def receive_district_info(self, border_len, border_wid):
        self.border_len = border_len
        self.border_wid = border_wid


class Direction:

    def forward(self):
        pass

    def turn_left(self):
        pass

class NDirection(Direction):
    pass

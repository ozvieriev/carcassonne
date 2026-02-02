from enum import Enum


class tileRotation(Enum):
    R0 = 0
    R90 = 90
    R180 = 180
    R270 = 270

    def rotate(self):
        value = (self.value + 90) % 360
        return tileRotation(value)
from time import time

import pygame.time


class Cooldown:
    def __init__(self):
        self.bTime = time()

    def calculate(self, delay, currentTime):
        newTime = currentTime - self.bTime
        newTime = round(newTime * 100)

        if newTime >= delay:
            return True
        else:
            return False


    def reset(self):
        self.bTime = time()


class Decay:
    def __init__(self):
        self.bTime = time()

    def bulletDecay(self, decayTime, object, currentTime):
        newTime = currentTime - self.bTime
        newTime = round(newTime * 100)

        if newTime >= decayTime:
            object.kill()
# noinspection PyUnresolvedReferences
import pygame
from utils import *


class Battery:
    def __init__(self, tier=0, pos: tuple[float, float] = (100, 100)):
        self.tier = tier  # 0 1 2 3 or 4 (case, teal, orange, blue, red)
        self.x, self.y = pos

    @property
    def pos(self):
        return self.x, self.y

    @pos.setter
    def pos(self, set_to: tuple[float, float]):
        self.x, self.y = set_to

    @property
    def image(self):
        return fetch_image("battery_" + ["case", "teal", "orange", "blue", "red"][self.tier] + ".png", (4, 4))

    @property
    def rect(self):
        return self.image.get_rect(center=self.pos)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)

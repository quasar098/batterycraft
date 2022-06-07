# noinspection PyUnresolvedReferences
import pygame
# noinspection PyUnresolvedReferences
from constants import *
from utils import *


class Foil:
    def __init__(self, pos: tuple[float, float]):
        self.x, self.y = pos
        self.oy = 0
        self.image = fetch_image("foil.png", (10, 10))

    @property
    def pos(self):
        return self.x, self.y+self.oy

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.image.get_rect(center=self.pos))

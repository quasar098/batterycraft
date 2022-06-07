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
        self.selected = False
        self.grab_position = (0, 0)

    @property
    def pos(self):
        return self.x, self.y+self.oy

    @property
    def rect(self):
        return self.image.get_rect(center=self.pos)

    def draw(self, screen: pygame.Surface):
        if self.selected:
            self.x = self.grab_position[0]+pygame.mouse.get_pos()[0]
            self.y = self.grab_position[1]+pygame.mouse.get_pos()[1]
        screen.blit(self.image, self.image.get_rect(center=self.pos))

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    self.selected = True
                    self.grab_position = self.x-pygame.mouse.get_pos()[0], self.y-pygame.mouse.get_pos()[1]
                    return True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.selected = False
                return True

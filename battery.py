# noinspection PyUnresolvedReferences
import pygame
from utils import *


class Battery:
    def __init__(self, tier=0, pos: tuple[float, float] = (100, 100), message=None):
        self.tier = tier  # 0 1 2 3 or 4 (case, teal, orange, blue, red)
        self.x, self.y = pos
        self.oy = 0
        self.grab_position = (0, 0)
        self.selected = False
        self.message = message
        self.rot = 0

    @property
    def pos(self):
        return self.x, self.y+self.oy

    @pos.setter
    def pos(self, set_to: tuple[float, float]):
        self.x, self.y = set_to

    @property
    def image(self):
        return fetch_image("battery_" + ["case", "teal", "orange", "blue", "red"][self.tier] + ".png", (4, 4),
                           rot=self.rot)

    @property
    def rect(self):
        return self.image.get_rect(center=self.pos)

    def draw(self, screen: pygame.Surface, font: pygame.font.Font = None):
        if self.selected:
            self.x = self.grab_position[0]+pygame.mouse.get_pos()[0]
            self.y = self.grab_position[1]+pygame.mouse.get_pos()[1]
        screen.blit(self.image, self.rect)
        if self.message is not None:
            if font is not None:
                mess = fetch_text(font, self.message, color=DARK_WHITE)
                mess_rect = mess.get_rect(midbottom=self.rect.midtop).move(0, -10)
                pygame.draw.rect(screen, DARKER_BLACK, mess_rect.inflate(6, 2))
                pygame.draw.rect(screen, BG_COLOR.lerp((255, 255, 255), 0.06), mess_rect.inflate(4, 0))
                screen.blit(mess, mess_rect)

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    self.selected = True
                    self.grab_position = self.x - pygame.mouse.get_pos()[0], self.y - pygame.mouse.get_pos()[1]
                    return True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.selected = False

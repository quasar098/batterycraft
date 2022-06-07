# noinspection PyUnresolvedReferences
import pygame
from utils import *
from constants import *


class Credits:
    def __init__(self, font: pygame.font.Font):
        self.texts = [
            "game by quasar098 and SnakMan",
            "art also by them",
            "uses pygame library",
            "not much else to say",
        ]
        self.surfaces = []
        for text in self.texts:
            self.surfaces.append(font.render(text, True, DARK_WHITE))
        self.back_rect = pygame.Rect(WIDTH-225, 25, 200, 100)
        self.font = font

    def draw(self, screen: pygame.Surface):
        for count, surf in enumerate(self.surfaces):
            y = count*50+25
            screen.blit(surf, (25, y))
        pygame.draw.rect(screen, ACCENT_COLOR, self.back_rect, border_radius=19)
        back_text = fetch_text(self.font, "go back")
        screen.blit(back_text, back_text.get_rect(center=self.back_rect.center))

    def handle_events(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # lmb pressed
                if self.back_rect.collidepoint(pygame.mouse.get_pos()):
                    set_current_screen("main menu")

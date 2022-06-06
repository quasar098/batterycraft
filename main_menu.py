import pygame
from constants import *
from utils import *


class MainMenu:
    def __init__(self, font: pygame.font.Font):
        self.font = font

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen)

    def handle_events(self, event: pygame.event.Event):
        pass

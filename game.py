# noinspection PyUnresolvedReferences
import pygame
# noinspection PyUnresolvedReferences
from utils import *
# noinspection PyUnresolvedReferences
from constants import *
from battery import Battery
from foil import Foil


class Game:
    def __init__(self, b_font, s_font):
        self.big_font = b_font
        self.s_font = s_font
        self.items = [Battery(0, (500, 400)), Foil((200, 400))]
        self.item_to_fill = "camera"

    def draw(self, screen: pygame.Surface):
        for item in self.items:
            item.draw(screen)

    @property
    def item_to_fill_image(self):
        if self.item_to_fill == "camera":
            return 0

    def handle_events(self, event: pygame.event.Event):
        for item in self.items.__reversed__():
            if item.handle_events(event):
                self.items.remove(item)
        if event.type == pygame.MOUSEBUTTONUP:
            for item in self.items:
                item.selected = False

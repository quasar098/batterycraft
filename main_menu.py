import pygame
from constants import *
from utils import *


class MainMenu:
    def __init__(self, font: pygame.font.Font):
        self.font = font
        self.play_rect = pygame.Rect((WIDTH/2-200, HEIGHT/2, 400, 100))
        self.credits_rect = pygame.Rect((WIDTH/2-200, HEIGHT/2+125, 400, 100))

    def draw(self, screen: pygame.Surface):
        # rects
        pygame.draw.rect(screen, ACCENT_COLOR, self.play_rect, border_radius=19)
        pygame.draw.rect(screen, ACCENT_COLOR, self.credits_rect, border_radius=19)

        play_game_text = fetch_text(self.font, "play game")
        credits_text = fetch_text(self.font, "credits")
        screen.blit(play_game_text, play_game_text.get_rect(center=self.play_rect.center))
        screen.blit(credits_text, credits_text.get_rect(center=self.credits_rect.center))

    def handle_events(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.play_rect.collidepoint(pygame.mouse.get_pos()):
                # play button clicked
                set_current_screen("game")
            if self.credits_rect.collidepoint(pygame.mouse.get_pos()):
                # credits button clicked
                set_current_screen("credits")

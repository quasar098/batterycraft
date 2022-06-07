# noinspection PyUnresolvedReferences
import pygame
# noinspection PyUnresolvedReferences
from constants import *
from utils import *
from battery import Battery


class MainMenu:
    def __init__(self, font: pygame.font.Font):
        self.font = font
        self.play_rect = pygame.Rect((WIDTH/2-200, HEIGHT/2, 400, 100))
        self.credits_rect = pygame.Rect((WIDTH/2-200, HEIGHT/2+125, 400, 100))
        self.left_battery = Battery(1, (200, HEIGHT/2))
        self.right_battery = Battery(4, (WIDTH-200, HEIGHT/2))
        self.logo_image = fetch_image("battery_craft.png", (20, 20))

    def draw(self, screen: pygame.Surface):
        # rects
        pygame.draw.rect(screen, ACCENT_COLOR, self.play_rect, border_radius=19)
        pygame.draw.rect(screen, ACCENT_COLOR, self.credits_rect, border_radius=19)

        play_game_text = fetch_text(self.font, "play game")
        credits_text = fetch_text(self.font, "credits")
        screen.blit(play_game_text, play_game_text.get_rect(center=self.play_rect.center))
        screen.blit(credits_text, credits_text.get_rect(center=self.credits_rect.center))

        # batteries
        tick = pygame.time.get_ticks()
        self.left_battery.y = HEIGHT/2+120+sin(tick/500)*50
        self.right_battery.y = HEIGHT/2+120+sin((tick+1000)/500)*50
        self.left_battery.draw(screen)
        self.right_battery.draw(screen)

        # title
        self.logo_image = fetch_image("battery_craft.png", (20, 20), rot=sin(tick/800)*10)
        screen.blit(self.logo_image, self.logo_image.get_rect(center=(WIDTH/2, 180)))

    def handle_events(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.play_rect.collidepoint(pygame.mouse.get_pos()):
                # play button clicked
                set_current_screen("game")
            if self.credits_rect.collidepoint(pygame.mouse.get_pos()):
                # credits button clicked
                set_current_screen("credits")

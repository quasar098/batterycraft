# noinspection PyUnresolvedReferences
import pygame
# noinspection PyUnresolvedReferences
from constants import *
from utils import *
from battery import Battery
from foil import Foil


class MainMenu:
    def __init__(self, font: pygame.font.Font):
        self.font = font
        self.play_rect = pygame.Rect((WIDTH/2-200, HEIGHT/2, 400, 100))
        self.credits_rect = pygame.Rect((WIDTH/2-200, HEIGHT/2+125, 400, 100))
        self.left_wheel = [Battery(4), Battery(1), Battery(3), Battery(2), Battery(2), Battery(3), Battery(2), Battery(3)]
        for count, battery in enumerate(self.left_wheel):
            battery.oy = count/2*HEIGHT-HEIGHT*2
            battery.tier = rand(0, 4)
        self.right_wheel = [Battery(4), Battery(1), Battery(3), Battery(2), Battery(2), Battery(3), Battery(2), Battery(3)]
        for count2, battery2 in enumerate(self.right_wheel):
            battery2.oy = count2/2*HEIGHT-HEIGHT*2+HEIGHT/4
            battery2.tier = rand(0, 4)
        self.logo_image = fetch_image("battery_craft.png", (20, 20))

    def draw(self, screen: pygame.Surface):
        # rects
        pygame.draw.rect(screen, ACCENT_COLOR, self.play_rect, border_radius=19)
        pygame.draw.rect(screen, ACCENT_COLOR, self.credits_rect, border_radius=19)

        play_game_text = fetch_text(self.font, "play game")
        credits_text = fetch_text(self.font, "credits")
        halfpos = (pygame.mouse.get_pos()[0]-WIDTH/2)/10+WIDTH/2
        screen.blit(play_game_text, play_game_text.get_rect(center=self.play_rect.center).move(
            clamp(halfpos, self.play_rect.left+100, self.play_rect.right-100)-self.play_rect.centerx, 0
        ))
        screen.blit(credits_text, credits_text.get_rect(center=self.credits_rect.center).move(
            clamp(halfpos, self.credits_rect.left+100, self.credits_rect.right-100)-
            self.credits_rect.centerx, 0
        ))

        # batteries
        tick = pygame.time.get_ticks()
        for item in self.left_wheel:
            item.y = 0
            item.draw(screen)
            item.x = 200
            item.oy += sin(tick/1000)*3+4
            if item.oy > HEIGHT*2:
                item.oy = -HEIGHT*2
                item.tier = rand(0, 4)
        for item in self.right_wheel:
            item.y = 0
            item.draw(screen)
            item.x = WIDTH-200
            item.oy += 4+sin((tick+3142)/1000)*3
            if item.oy > HEIGHT*2:
                item.oy = -HEIGHT*2
                item.tier = rand(0, 4)

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

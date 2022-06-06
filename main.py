from utils import *
import pygame
from constants import *
from main_menu import MainMenu

pygame.init()

screen = pygame.display.set_mode([WIDTH, HEIGHT])
big_font = pygame.font.Font(get_path("kdamthmorpro.ttf"), 32)
small_font = pygame.font.Font(get_path("kdamthmorpro.ttf"), 16)
clock = pygame.time.Clock()

main_menu = MainMenu(big_font)

running = True
while running:
    screen.fill(BG_COLOR)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        main_menu.handle_events(event)

    # code here
    main_menu.draw(screen)

    pygame.display.flip()
    clock.tick(FRAMERATE)
pygame.quit()

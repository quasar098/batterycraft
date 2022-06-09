from utils import *
import pygame
from constants import *
from main_menu import MainMenu
from credits import Credits
from game import Game
from highscores import Highscores

pygame.mixer.init()
play_sound("music.mp3", 0.2, True)

pygame.init()

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("batterycraft")
pygame.display.set_icon(pygame.image.load(get_path("favicon.ico")))
big_font = pygame.font.Font(get_path("kdamthmorpro.ttf"), 32)
small_font = pygame.font.Font(get_path("kdamthmorpro.ttf"), 16)
clock = pygame.time.Clock()

main_menu = MainMenu(big_font)
creds = Credits(big_font)
game = Game(big_font, small_font)
highscores = Highscores(big_font)

load_highscores()

running = True
while running:
    screen.fill(BG_COLOR)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if get_current_screen() == "game":
            game.handle_events(event)
            continue
        if get_current_screen() == "main menu":
            main_menu.handle_events(event)
        if get_current_screen() == "credits":
            creds.handle_events(event)
        if get_current_screen() == "highscores":
            highscores.handle_events(event)

        # particles and whatnot
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for _ in range(10):
                    add_particle(pygame.mouse.get_pos(), 7, ACCENT_COLOR)
                play_sound("electricity1.wav", 0.03)

    # main menu
    if get_current_screen() == "main menu":
        main_menu.draw(screen)
        if game.money >= game.money_goal:
            game = Game(big_font, small_font)
    if get_current_screen() == "credits":
        creds.draw(screen)
    if get_current_screen() == "game":
        game.draw(screen)
    if get_current_screen() == "highscores":
        highscores.draw(screen)

    update_particles(screen)
    calm_shake()
    new = screen.copy()
    screen.fill(BG_COLOR)
    screen.blit(new, (get_shake()))
    pygame.display.flip()
    clock.tick(FRAMERATE)
pygame.quit()
save_highscores()

from utils import *


class Highscores:
    def __init__(self, big_font: pygame.font.Font):
        self.font = big_font

    def draw(self, screen: pygame.Surface) -> None:
        click_again_text = fetch_text(self.font, "Click to go back to the main menu", DARK_WHITE)
        screen.blit(click_again_text, (10, 10))

        highscores_label = fetch_text(self.font, "HIGHSCORES:", DARK_WHITE)
        screen.blit(highscores_label, (10, 70))

        if len(get_highscores()) == 0:
            screen.blit(fetch_text(self.font, "no scores how??", DARK_WHITE), (10, 120))
        for y, score in enumerate(get_highscores()):
            screen.blit(fetch_text(self.font, f"{score}s", DARK_WHITE), (10, 120+y*50))

    # noinspection PyMethodMayBeStatic
    def handle_events(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                set_current_screen("main menu")

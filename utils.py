from os import getcwd
from os.path import join
from constants import *
from screen_manager import set_current_screen, get_current_screen
import pygame


def get_path(*path: str):
    return join(getcwd(), "assets", *path)


text_storage: dict[str, pygame.Surface] = {}
image_storage: dict[str, pygame.Surface] = {}


def fetch_text(font: pygame.font.Font, text: str):
    if text not in text_storage:
        text_storage[text] = font.render(text, True, DARKER_BLACK)
    return text_storage[text]


def fetch_image(name, resize=(1, 1)):
    serialized = f"{name}|{resize}"
    if serialized not in image_storage:
        image_storage[serialized] = pygame.image.load(get_path(name)).convert_alpha()
        if resize != (1, 1):
            size = list(image_storage[serialized].get_size())
            size[0] *= resize[0]
            size[1] *= resize[1]
            image_storage[serialized] = pygame.transform.scale(image_storage[serialized], size)
    return image_storage[serialized]

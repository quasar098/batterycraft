from os import getcwd
from os.path import join
from constants import *
import pygame


def get_path(*path: str):
    return join(getcwd(), "assets", *path)


text_storage: dict[str, pygame.Surface] = {}
image_storage: dict[str, pygame.Surface] = {}


def fetch_text(font: pygame.font.Font, text: str):
    if text not in text_storage:
        text_storage[text] = font.render(text, True, DARK_WHITE)
    return text_storage[text]


def fetch_image(*path):
    if str(path) in image_storage:
        image_storage[str(path)] = pygame.image.load(*path).convert_alpha()
    return image_storage[str(path)]
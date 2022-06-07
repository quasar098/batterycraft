from os import getcwd
from os.path import join
from constants import *
# noinspection PyUnresolvedReferences
from screen_manager import set_current_screen, get_current_screen
# noinspection PyUnresolvedReferences
from numpy import clip as clamp
# noinspection PyUnresolvedReferences
from random import uniform as randr, randint as rand
# noinspection PyUnresolvedReferences
from particles import add_particle, update_particles
import pygame
# noinspection PyUnresolvedReferences
from math import sin


shake = [0, 0]


def get_shake():
    return randr(-shake[0], shake[0]), randr(-shake[1], shake[1])


def calm_shake():
    shake[0] *= 0.96
    shake[1] *= 0.96


def add_shake(shake2: tuple[float, float]):
    shake[0] += shake2[0]
    shake[1] += shake2[1]


def get_path(*path: str):
    return join(getcwd(), "assets", *path)


text_storage: dict[str, pygame.Surface] = {}
image_storage: dict[str, pygame.Surface] = {}


def fetch_text(font: pygame.font.Font, text: str):
    if text not in text_storage:
        text_storage[text] = font.render(text, True, DARKER_BLACK)
    return text_storage[text]


def fetch_image(name, resize=(1, 1), rot=0):
    serialized = f"{name}|{resize}|{rot}"
    if serialized not in image_storage:
        image_storage[serialized] = pygame.image.load(get_path(name)).convert_alpha()
        if resize != (1, 1):
            size = list(image_storage[serialized].get_size())
            size[0] *= resize[0]
            size[1] *= resize[1]
            image_storage[serialized] = pygame.transform.scale(image_storage[serialized], size)
        if rot != 0:
            image_storage[serialized] = pygame.transform.rotate(image_storage[serialized], rot)
    return image_storage[serialized]

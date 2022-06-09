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
# noinspection PyUnresolvedReferences
from time import time
from json import load, dump


shake = [0, 0]
highscores_values = []


def get_shake():
    return randr(-shake[0], shake[0]), randr(-shake[1], shake[1])


def calm_shake():
    shake[0] *= 0.92
    shake[1] *= 0.92


def add_shake(shake2: tuple[float, float]):
    shake[0] += shake2[0]
    shake[1] += shake2[1]


def get_highscores():
    highscores_values.sort(reverse=True)
    return highscores_values


def add_highscore(ta: float):
    highscores_values.append(ta)


def save_highscores():
    with open(get_path("save_data.json"), 'w') as f:
        dump({"highscores": highscores_values}, f)


def load_highscores():
    global highscores_values
    try:
        with open(get_path("save_data.json"), 'r') as f:
            highscores_values = load(f).get("highscores", [])
    except FileNotFoundError:
        save_highscores()
        load_highscores()


def get_path(*path: str):
    return join(getcwd(), "assets", *path)


text_storage: dict[str, pygame.Surface] = {}
image_storage: dict[str, pygame.Surface] = {}
sound_storage: dict[str, pygame.mixer.Sound] = {}
channels: list[pygame.mixer.Channel] = []


def fetch_text(font: pygame.font.Font, text: str, color: pygame.Color = DARKER_BLACK):
    serialized = f"{text}|{color}"
    if serialized not in text_storage:
        text_storage[serialized] = font.render(text, True, color)
    return text_storage[serialized]


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


def play_sound(name: str, vol: float = 0.2, loop=0) -> bool:
    """Returns true if the sound was successfully played"""
    if len(channels) == 0:
        for _ in range(8):
            channels.append(pygame.mixer.Channel(_))
    if name not in sound_storage:
        sound_storage[name] = pygame.mixer.Sound(get_path(name))
    chan = pygame.mixer.find_channel(False)
    if chan is not None:
        chan.set_volume(vol)
        chan.play(sound_storage[name], -loop)
        return True
    return False

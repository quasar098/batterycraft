# noinspection PyUnresolvedReferences
import pygame
# noinspection PyUnresolvedReferences
from constants import *
from utils import *
from typing import Union
from battery import Battery
from math import sqrt


class Rechargeable:
    def __init__(self):
        self.x = WIDTH-250
        self.y = HEIGHT/2
        self.glue_radius = 40

        # CHANGE THESE WHEN INHERITING
        self.image_prefix = "rechargeable"
        self.glue_spots: dict[tuple[int, int, int], Union[None, Battery]] = {}
        self.charge_required = 1
        self.reward = 0

    def offset_by_topleft(self, pos: tuple[int, int, int]):
        return pos[0]*4+self.rect.left, pos[1]*4+self.rect.top

    @property
    def image(self):
        return fetch_image(f"{self.image_prefix}{self.total_charge}.png", (4, 4))

    def glue_check(self, battery: Battery):
        """Return true if was able to stick a battery inside the rechargeable"""
        def theorem(p1, p2): return sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)
        best_contender = None
        best_score = self.glue_radius
        for glue_spot in self.glue_spots:
            distance = theorem(battery.pos, self.offset_by_topleft(glue_spot))
            if self.glue_spots[glue_spot] is None:
                if distance < best_score:
                    best_contender = glue_spot
                    best_score = distance
        if best_contender is not None:
            self.glue_spots[best_contender] = battery
            return True
        return False

    @property
    def total_charge(self):
        return clamp(sum([(self.glue_spots[glue_spot].tier if self.glue_spots[glue_spot] is not None else 0)
                          for glue_spot in self.glue_spots]), 0, self.charge_required)

    @property
    def pos(self):
        return self.x, self.y

    @property
    def rect(self):
        return self.image.get_rect(center=self.pos)

    def draw_batteries(self, screen: pygame.Surface):
        for spot in self.glue_spots:
            if self.glue_spots[spot] is not None:
                self.glue_spots[spot].x, self.glue_spots[spot].y, self.glue_spots[spot].rot = spot
                self.glue_spots[spot].x *= 4
                self.glue_spots[spot].y *= 4
                self.glue_spots[spot].x += self.rect.left
                self.glue_spots[spot].y += self.rect.top
                self.glue_spots[spot].draw(screen)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)
        self.draw_batteries(screen)

    def handle_events(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for spot in self.glue_spots:
                    if self.glue_spots[spot] is not None:
                        if self.glue_spots[spot].rect.collidepoint(pygame.mouse.get_pos()):
                            bat = self.glue_spots[spot]
                            self.glue_spots[spot] = None
                            return bat
        return False

    def running(self) -> bool:
        return self.charge_required == self.total_charge and \
               all([self.glue_spots[spot] is not None for spot in self.glue_spots])


class Flashlight(Rechargeable):
    def __init__(self):
        super().__init__()
        self.image_prefix = "flashlight"
        self.glue_spots = {(64, 66, 0): None}
        self.charge_required = 1
        self.reward = rand(6, 10)


class Blender(Rechargeable):
    def __init__(self):
        super().__init__()
        self.image_prefix = "blender"
        self.glue_spots = {(64, 82, 90): None}
        self.charge_required = 4
        self.reward = rand(8, 16)


class Camera(Rechargeable):
    def __init__(self):
        super().__init__()
        self.image_prefix = "camera"
        self.glue_spots = {(24, 72, 0): None, (44, 72, 0): None, (64, 72, 0): None, (84, 72, 0): None}
        self.charge_required = 5
        self.reward = rand(8, 16)


class Radio(Rechargeable):
    def __init__(self):
        super().__init__()
        self.image_prefix = "radio"
        self.glue_spots = {(84, 71, 0): None, (104, 71, 0): None}
        self.charge_required = 6
        self.reward = rand(8, 16)

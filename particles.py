# noinspection PyUnresolvedReferences
import pygame
# noinspection PyUnresolvedReferences
from constants import *
from utils import *


particles = []


class Particle:
    def __init__(self, pos, size, color, dy):
        self.age = size
        self.x, self.y = pos
        self.dx, self.dy = randr(-2, 2), dy + randr(0, 2)
        self.color = color
        self.decay_rate = randr(0.1, 0.2)
        self.gravity = randr(0.1, 0.3)

    def draw(self, screen: pygame.Surface):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.age)
        self.age -= self.decay_rate
        self.x += self.dx
        self.y += self.dy
        self.dy += self.gravity


def add_particle(pos: tuple[float, float], size: int, color: tuple[int, int, int], dy=-5):
    particles.append(Particle(pos, size, color, dy=dy))


def update_particles(screen: pygame.Surface):
    global particles
    for particle in particles:
        particle.draw(screen)
    particles = [particle for particle in particles if particle.age > 0]

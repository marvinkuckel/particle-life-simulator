### particle.py 

import random # for random number generation
import pygame # for creating a window, graphics, handling events etc.


class Particle:
    def __init__(self, type, color, size, position, velocity, friction, random_movement):
        self.type = type
        self.color = color
        self.size = size
        self.position = position
        self.velocity = velocity
        self.friction = friction
        self.random_movement = random_movement

    def update(self):
        # updates position based on velocity
        self.position = (self.position[0] + self.velocity[0], self.position[1] + self.velocity[1])
        # updates position based on random movement
        self.position = (self.position[0] + random.uniform(-self.random_movement, self.random_movement),
                         self.position[1] + random.uniform(-self.random_movement, self.random_movement))
        # updates velocity based on friction
        self.velocity = (self.velocity[0] * self.friction, self.velocity[1] * self.friction)
        # implement bouncing back at edges
        pass

    def draw(self, screen):
        # draws particle on the screen created by pygame
        pygame.draw.circle(screen, self.color, (int(self.position[0]), int(self.position[1])), self.size)

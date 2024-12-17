import random  # for random number generation
import pygame  # for creating a window, graphics, handling events etc.


class Particle:
    def __init__(self, type, color, size, position, velocity = [0, 0], friction = 0, random_movement = 0):
        self.type = type
        self.color = color
        self.size = size
        self.position = position
        self.velocity = velocity
        self.friction = friction
        self.random_movement = random_movement

    def update(self, dt, time_factor):
        # updates position based on velocity
        self.position = [self.position[0] + self.velocity[0] * dt * time_factor, 
                        self.position[1] + self.velocity[1] * dt * time_factor]
        # updates position based on random movement
        if self.random_movement != 0:
            rand_x = random.uniform(-self.random_movement, self.random_movement) * time_factor
            rand_y = random.uniform(-self.random_movement, self.random_movement) * time_factor
            self.position = [self.position[0] + rand_x, self.position[1] + rand_y]
        # updates velocity based on friction
        self.velocity = [self.velocity[0] * (1 - self.friction), 
                        self.velocity[1] * (1 - self.friction)]

    def draw(self, screen, screen_width, screen_height, colors):
        # draws particle on the screen created by pygame
        pygame.draw.circle(screen, colors[self.type], (int(self.position[0] * screen_height), int(self.position[1] * screen_height)), self.size)
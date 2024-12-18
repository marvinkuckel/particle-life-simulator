import random
import pygame

class Particle:
    def __init__(self, type, color, size, position, velocity=[0, 0], friction=0, random_movement=0):
        self.type = type
        self.color = color
        self.size = size
        self.position = position
        self.velocity = velocity
        self.friction = friction
        self.random_movement = random_movement

    def update(self, dt, time_factor):
        # Updates position based on velocity
        self.position = [self.position[0] + self.velocity[0] * dt * time_factor, 
                         self.position[1] + self.velocity[1] * dt * time_factor]

        # Updates position based on random movement
        if self.random_movement != 0:
            rand_x = random.uniform(-self.random_movement, self.random_movement) * time_factor
            rand_y = random.uniform(-self.random_movement, self.random_movement) * time_factor
            self.position = [self.position[0] + rand_x, self.position[1] + rand_y]

        # Updates velocity based on friction
        self.velocity = [self.velocity[0] * (1 - self.friction), 
                         self.velocity[1] * (1 - self.friction)]

        # Check for boundary collisions and reverse velocity if necessary
        if self.position[0] <= 0 or self.position[0] >= 1:
            self.velocity[0] = -self.velocity[0]
        if self.position[1] <= 0 or self.position[1] >= 1:
            self.velocity[1] = -self.velocity[1]

        # Keep position within the [0, 1] range
        self.position[0] = max(0, min(self.position[0], 1))
        self.position[1] = max(0, min(self.position[1], 1))

    def draw(self, screen, screen_width, screen_height, colors):
        # Draws the particle on the screen
        pygame.draw.circle(screen, colors[self.type], 
                           (int(self.position[0] * screen_width), int(self.position[1] * screen_height)), self.size)
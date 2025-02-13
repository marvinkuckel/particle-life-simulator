import random
import pygame

class Particle:
    def __init__(self, type: int, size, position, velocity=[0, 0], friction=0, random_movement=0):
        self.type = type
        self.size = size
        self.position = position
        self.velocity = velocity
        self.friction = friction
        self.random_movement = random_movement


    def apply_force(self, force_x, force_y, scaling = 0.03):
        self.velocity = [self.velocity[0] + force_x*scaling, self.velocity[1] + force_y*scaling]

    def update_position(self, dt, time_factor):
        # update velocity based on applied friction
        self.velocity = [self.velocity[0] * (1 - self.friction),
                        self.velocity[1] * (1 - self.friction)]

        # update position based on new velocity
        self.position = [self.position[0] + self.velocity[0] * dt * time_factor,
                        self.position[1] + self.velocity[1] * dt * time_factor]

        # update position based on random movement
        if self.random_movement:
            rand_x = random.uniform(-self.random_movement, self.random_movement) * time_factor
            rand_y = random.uniform(-self.random_movement, self.random_movement) * time_factor
            self.position = [self.position[0] + rand_x, self.position[1] + rand_y]

    def draw(self, screen, screen_width, screen_height, color):
        # Draws the particle on the screen
        pygame.draw.circle(screen, color, radius = self.size,
                           center=(self.position[0] * screen_width,
                                   self.position[1] * screen_height))

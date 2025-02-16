import random
import pygame


class Particle:
    def __init__(self, type: int, size: int, position: tuple, velocity: tuple, friction: float, force_scaling: float):
        self.type = type
        self.size = size
        self.position = position
        self.velocity = velocity
        self.friction = friction
        self.force_scaling = force_scaling
     

    def apply_force(self, force_x, force_y):
        self.velocity = [self.velocity[0] + force_x*self.force_scaling, self.velocity[1] + force_y*self.force_scaling]

    def update_position(self, dt, time_factor):
        # update velocity based on applied friction
        self.velocity = [self.velocity[0] * (1 - self.friction),
                        self.velocity[1] * (1 - self.friction)]

        # update position based on new velocity
        self.position = [self.position[0] + self.velocity[0] * dt * time_factor,
                        self.position[1] + self.velocity[1] * dt * time_factor]


    def draw(self, screen, screen_width, screen_height, color):
        # Draws the particle on the screen
        pygame.draw.circle(screen, color, radius = self.size,
                           center=(self.position[0] * screen_width,
                                   self.position[1] * screen_height))

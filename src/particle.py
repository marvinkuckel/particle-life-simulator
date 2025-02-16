import random
import pygame


class Particle:
    def __init__(self, type: int, size: int, position: tuple, velocity: tuple, friction: float, force_scaling: float, random_movement: float):
        self.type = type
        self.size = size
        self.position = position
        self.velocity = velocity
        self.friction = friction
        self.force_scaling = force_scaling          
        self.random_movement = random_movement
        self.last_render_position = tuple(position) # tracks particles last rendered position


    def apply_force(self, force_x, force_y):
        # applies force and the scaling factor to current velocity
        self.velocity = [self.velocity[0] + force_x*self.force_scaling, self.velocity[1] + force_y*self.force_scaling]


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


    def draw(self, screen, screen_width, screen_height, color, threshold=0.001):  
        # particles movement since last render
        dx = abs(self.position[0] - self.last_render_position[0])
        dy = abs(self.position[1] - self.last_render_position[1])

        # only updates rendered position if above threshold
        if dx > threshold or dy > threshold:
            self.last_render_position = self.position

        # conversion to screen coordinates
        draw_x = round(self.last_render_position[0] * screen_width)
        draw_y = round(self.last_render_position[1] * screen_height)

        # draws the particle
        pygame.draw.circle(screen, color, (draw_x, draw_y), self.size)
        
    

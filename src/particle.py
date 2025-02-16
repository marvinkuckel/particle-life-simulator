import random
import pygame

class Particle:
    def __init__(self, type: int, size: int, position: tuple, velocity: tuple, friction: float, force_scaling: float, random_movement: float):
        """
        Initializes a particle with given properties.
        type: Identifier for the particle type.
        size: Radius of the particles.
        position: Initial position of the particle.
        velocity: Initial velocity of the particle.
        friction: Friction coefficient for the particle.
        random_movement: Magnitude of random movement for the particle.
        """
        self.type = type
        self.size = size
        self.position = position
        self.velocity = velocity
        self.friction = friction
        self.force_scaling = force_scaling          
        self.random_movement = random_movement
        self.last_render_position = tuple(position) # Tracks particles last rendered position

    def apply_force(self, force_x, force_y):
        """
        Applies a force to the particle, adjusting its velocity accordingly.
        force_x: Force applied in the x-direction.
        force_y: Force applied in the y-direction.
        scaling: Scaling factor to regulate the impact of the force.
        """
        self.velocity = [self.velocity[0] + force_x*self.force_scaling, self.velocity[1] + force_y*self.force_scaling]

    def update_position(self, dt, time_factor):
        """
        Reduces the velocity of the particle based on its friction.
        Updates the position of the particle based on its velocity and friction.
        dt: Time since the last update.
        time_factor: Scaling factor to adjust the speed of the simulation.
        """
        self.velocity = [self.velocity[0] * (1 - self.friction),  # Reduce velocity in x direction based on friction
                        self.velocity[1] * (1 - self.friction)]  # Reduce velocity in y direction based on friction

        self.position = [self.position[0] + self.velocity[0] * dt * time_factor,  # Update position in x direction
                        self.position[1] + self.velocity[1] * dt * time_factor]  # Update position in y direction
        
        # Update position based on random movement
        if self.random_movement:  # If random movement is enabled...
            rand_x = random.uniform(-self.random_movement, self.random_movement) * time_factor  # Random velocity in the x-direction
            rand_y = random.uniform(-self.random_movement, self.random_movement) * time_factor  # Random velocity in the y-direction
            self.position = [self.position[0] + rand_x, self.position[1] + rand_y]

    def draw(self, screen, screen_width, screen_height, color, threshold=0.001):  
        """
        Draws the particle as a circle on the given Pygame screen.
        screen: Pygame screen to draw on.
        screen_width: Width of the Pygame screen.
        screen_height: Height of the Pygame screen.
        color: Color of the particle.
        """
        dx = abs(self.position[0] - self.last_render_position[0])
        dy = abs(self.position[1] - self.last_render_position[1])

        # Only updates rendered position if above threshold
        if dx > threshold or dy > threshold:
            self.last_render_position = self.position

        # Conversion to screen coordinates
        draw_x = round(self.last_render_position[0] * screen_width)
        draw_y = round(self.last_render_position[1] * screen_height)

        # Draws the particle
        pygame.draw.circle(screen, color, (draw_x, draw_y), self.size)

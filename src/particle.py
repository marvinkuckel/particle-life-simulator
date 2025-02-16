import random
import pygame

class Particle:
    def __init__(self, type: int, size, position, velocity=[0, 0], friction=0, random_movement=0):
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
        self.random_movement = random_movement

    def apply_force(self, force_x, force_y, scaling = 0.03):
        """
        Applies a force to the particle, adjusting its velocity accordingly.
        force_x: Force applied in the x-direction.
        force_y: Force applied in the y-direction.
        scaling: Scaling factor to regulate the impact of the force.
        """
        self.velocity = [self.velocity[0] + force_x * scaling, self.velocity[1] + force_y * scaling]  # Apply force to velocity

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

        if self.random_movement:  # If random movement is enabled...
            rand_x = random.uniform(-self.random_movement, self.random_movement) * time_factor  # Random velocity in the x-direction
            rand_y = random.uniform(-self.random_movement, self.random_movement) * time_factor  # Random velocity in the y-direction
            self.position = [self.position[0] + rand_x, self.position[1] + rand_y]

    def draw(self, screen, screen_width, screen_height, color):
        """
        Draws the particle as a circle on the given Pygame screen.
        screen: Pygame screen to draw on.
        screen_width: Width of the Pygame screen.
        screen_height: Height of the Pygame screen.
        color: Color of the particle.
        """
        pygame.draw.circle(screen, color, radius = self.size,  # Draw particle
                            center=(self.position[0] * screen_width,  # Convert the x-position (relative) to screen coordinates
                            self.position[1] * screen_height))  # Convert the y-position (relative) to screen coordinates

"""
The simulation.py file will contain the Simulation class responsible for creating and updating
particles, handling their interactions, and ensuring the simulation performs efficiently. This class will
interact with the particle.py and interactions.py files to manage particle properties and rules.
"""

import pygame
from particle import Particle
from interactions import InteractionMatrix
import random

class Simulation:
    def __init__(self, width, height, num_particles = 200):
        self.width = width
        self.height = height
        self.num_particles = num_particles
        self.particles = []
        self.running = False

    def setup_simulation(self):
        """
        Sets up the initial state of the simulation, including creating particles.
        """
        for _ in range(self.num_particles):
            self.particles.append(Particle(
                type=0,
                color=(255, 255, 255),
                size=3,
                position=(random.randint(0, self.width), random.randint(0, self.height)),
                velocity=(random.uniform(-1, 1), random.uniform(-1, 1)),
                friction=0.99,
                random_movement=0.5
            ))

    def render_frame(self, screen):
        """
        Draws the current state of the simulation onto the screen.
        """
        for particle in self.particles:
            particle.draw(screen)

    def update_simulation(self):
        """
        Updates the state of the simulation by calculating particle interactions,
        applying rules, and updating particle positions.
        """
        if not self.running:
            return
        for particle in self.particles:
            particle.update()

    def enforce_boundaries(self):
        """
        Ensures that particles stay within the defined simulation boundaries.
        """
        pass

"""
The simulation.py file will contain the Simulation class responsible for creating and updating
particles, handling their interactions, and ensuring the simulation performs efficiently. This class will
interact with the particle.py and interactions.py files to manage particle properties and rules.
"""
import random

import pygame
from particle import Particle
from interactions import InteractionMatrix

class Simulation:
    def __init__(self, width, height, num_particles = 2000):
        """
        Initializes the simulation with the specified dimensions and number of particles.

        width: The width of the simulation area.
        height: The height of the simulation area.
        num_particles: The number of particles to generate.
        """
        self.width = width
        self.height = height
        
        self.setup_simulation()

    def setup_simulation(self, num_types: int):
        """
        Sets up the initial state of the simulation, including creating particles.
        """
        self.particles = [Particle(type = i % num_types, color=None, size=1, 
                                   position=(random.random(), random.random),
                                   velocity=(1 - random.random*2, 1 - random.random*2), 
                                   friction=0, random_movement=0) for i in range(self.num_particles)]
        pass

    def render_frame(self, screen: pygame.display):
        """
        Draws the current state of the simulation onto the screen.
        """
        for p in self.particles:
            p.draw(screen)

    def update(self, dt):
        """
        Updates the state of the simulation by calculating particle interactions,
        applying rules, and updating particle positions.
        """
        for p in self.particles:
            p.update()
            
        self.enforce_boundaries()

    def enforce_boundaries(self):
        """
        Ensures that particles stay within the defined simulation boundaries.
        """
        for p in self.particles:
            if p.position[0] < 0 or p.position[0] > 1:
                p.velocity[0] = -p.velocity[0]
                
            if p.position[1] < 0 or p.position[1] > 1:
                p.velocity[1] = -p.velocity[1]
            
            
        

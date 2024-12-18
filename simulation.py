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
    def __init__(self, width, height, num_particles = 2000, num_types = 4, time_factor=0.0001):
        """
        Initializes the simulation with the specified dimensions and number of particles.

        width: The width of the simulation area.
        height: The height of the simulation area.
        num_particles: The number of particles to generate.
        """
        self.width = width
        self.height = height
        self.num_particles = num_particles
        self.num_types = num_types
        self.time_factor = time_factor
        
        self.setup_simulation()

    def setup_simulation(self):
        """
        Sets up the initial state of the simulation, including creating particles.
        """
        self.particles = [Particle(type = i % self.num_types, color=(255,255,255), size=1, 
                                   position=(random.random(), random.random()),
                                   velocity=(1 - random.random()*2, 1 - random.random()*2), 
                                   friction=0, random_movement=0) for i in range(self.num_particles)]
        pass

    def render_frame(self, screen: pygame.display, colors):
        """
        Draws the current state of the simulation onto the screen.
        """
        for p in self.particles:
            p.draw(screen, self.width, self.height, colors)

    def update(self, dt):
        """
        Updates the state of the simulation by calculating particle interactions,
        applying rules, and updating particle positions.
        """
        for p in self.particles:
            p.update(dt, self.time_factor)
            
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
            
            
        

"""
The simulation.py file will contain the Simulation class responsible for creating and updating
particles, handling their interactions, and ensuring the simulation performs efficiently. This class will
interact with the particle.py and interactions.py files to manage particle properties and rules.
"""

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
        self.num_particles = num_particles

    def setup_simulation(self):
        """
        Sets up the initial state of the simulation, including creating particles.
        """
        pass

    def render_frame(self):
        """
        Draws the current state of the simulation onto the screen.
        """
        pass

    def update_simulation(self):
        """
        Updates the state of the simulation by calculating particle interactions,
        applying rules, and updating particle positions.
        """
        pass

    def enforce_boundaries(self):
        """
        Ensures that particles stay within the defined simulation boundaries.
        """
        pass

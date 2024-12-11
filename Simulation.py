"""
The simulation.py file will contain the Simulation class responsible for creating and updating
particles, handling their interactions, and ensuring the simulation performs efficiently. This class will
interact with the particle.py and interactions.py files to manage particle properties and rules.
"""

import pygame
from particle import Particle
from interactions import InteractionMatrix
from particle import Particle
import random


class Simulation:
    def __init__(self, width, height, num_particles = 200):
        self.width = width
        self.height = height
        self.num_particles = num_particles
        self.particles = []
        self.running = False
        self.interaction_matrix = InteractionMatrix(number_of_types=3, interaction_radius=50)

    def setup_simulation(self):
        """
        Sets up the initial state of the simulation, including creating particles.
        """
        for _ in range(self.num_particles):
            self.particles.append(Particle(
                type=random.randint(0, 3),       #4 different types of particles
                color=(200, 150, 100, 50),
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
        for particle in self.particles:
            net_force = [0, 0]
            for other in self.particles:
                if particle != other:
                    force = self.interaction_matrix.calculate_force(particle, other)
                    net_force[0] += force[0]
                    net_force[1] += force[1]
            particle.apply_force(net_force)
        
        #upade particle positions
        for particle in self.particles:
            particle.update(boundaries=(self.width, self.height))


    def enforce_boundaries(self):
        """
        Ensures that particles stay within the defined simulation boundaries.
        """
        pass
    
    def start_simulation(self):
        self.running = True

    def pause_simulation(self):
        self.running = False

    def reset(self):
        self.particles = []
        self.setup_simulation()

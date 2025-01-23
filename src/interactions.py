import random

from particle import Particle

class InteractionMatrix:
    def __init__(self, num_types: int, default_radius: float):
        self.default_radius = default_radius
        self.interactions = {
            (i, j): [random.choice((1, -1)) * 0.5, self.default_radius, 1.0]  # Default strength is 1.0 (no attraction)
            for i in range(num_types) for j in range(num_types)
        }

    def add_attraction(self, type1, type2, strength):
        # Set an attraction force between two types of particles
        if type1 != type2:  # Typically, attraction is between different types
            self.interactions[(type1, type2)][2] = strength
            self.interactions[(type2, type1)][2] = strength  # Symmetric interaction

    def calculate_force(self, p1, p2):
        force, radius, attraction = self.interactions[p1.type, p2.type]
        distance = self._distance(p1.position, p2.position)

        if distance <= radius:
            applied_force = (force / distance ** 2) - attraction  # Apply attraction force
            x_force = (p2.position[0] - p1.position[0]) * applied_force
            y_force = (p2.position[1] - p1.position[1]) * applied_force
            return x_force, y_force
        return 0, 0

    @staticmethod
    def _distance(p1_pos, p2_pos):
        return ((p2_pos[0] - p1_pos[0]) ** 2 + (p2_pos[1] - p1_pos[1]) ** 2) ** 0.5

    interactions: dict[(int, int), float]

    def __init__(self, number_of_types: int, default_interaction_radius: float):
        self.default_interaction_radius = default_interaction_radius
        
        self.interactions = {
            (i, j): [random.choice((1, -1))*0.5, self.default_interaction_radius]
            for i in range(number_of_types)
            for j in range(number_of_types)
        }
        
    def calculate_force(self, p1: Particle, p2: Particle):
        force, radius = self.interactions[p1.type, p2.type]
        
        distance = self._distance(p1.position, p2.position)
        if distance <= radius:
            if distance > 0.005:
                applied_force = (force / distance**2)-force# if distance < 1 else (force * distance**3)
                x_force = (p2.position[0] - p1.position[0]) * applied_force
                y_force = (p2.position[1] - p1.position[1]) * applied_force
            else:
                applied_force = 1 / ((distance+0.000001)**(distance))
                x_force = -(p2.position[0] - p1.position[0]) * applied_force
                y_force = -(p2.position[1] - p1.position[1]) * applied_force
            return x_force, y_force
        return 0, 0

    def _distance(self, p1_pos, p2_pos):
        return ((p2_pos[0] - p1_pos[0])**2 + (p2_pos[1] - p1_pos[1])**2)**0.5

   # Beispiel: Anziehungskraft zwischen Partikeln vom Typ 0 und 1 mit einer Stärke von 0.1
# tests/test_interaction_matrix.py
import pytest


from .interaction_matrix import InteractionMatrix

from src.particle import Particle

def test_calculate_force_no_interaction():
    interaction_matrix = InteractionMatrix(num_types=4, default_radius=0.05)
    p1 = Particle(type_id=0, size=2, position=(0.1, 0.1))
    p2 = Particle(type_id=1, size=2, position=(0.1, 0.2))
    
    # Keine Wechselwirkung, wenn die Distanzen zu groß sind
    force_x, force_y = interaction_matrix.calculate_force(p1, p2)
    assert force_x == 0
    assert force_y == 0

def test_calculate_force_with_interaction():
    interaction_matrix = InteractionMatrix(num_types=4, default_radius=0.1)
    p1 = Particle(type_id=0, size=2, position=(0.1, 0.1))
    p2 = Particle(type_id=1, size=2, position=(0.1, 0.15))
    
    # Berechnung der Wechselwirkung, wenn die Distanzen klein genug sind
    force_x, force_y = interaction_matrix.calculate_force(p1, p2)
    assert force_x != 0
    assert force_y != 0


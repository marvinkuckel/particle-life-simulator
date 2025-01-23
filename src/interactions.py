import random
from particle import Particle

# src/particle.py

class Particle:
    def __init__(self, type_id: int, size: int, position: tuple):
        self.type = type_id  # Partikeltyp
        self.size = size  # Partikelgröße
        self.position = position  # Position des Partikels als Tupel (x, y)


class InteractionMatrix:
    def __init__(self, num_types: int, default_radius: float):
        self.default_radius = default_radius
        # Erstellen der Interaktionsmatrix
        self.interactions = {
            (i, j): [random.choice((1, -1)) * 0.5, self.default_radius, 1.0]  # Default strength is 1.0 (no attraction)
            for i in range(num_types) for j in range(num_types)
        }

    def add_attraction(self, type1, type2, strength):
        # Setzt eine Anziehungswirkung zwischen zwei Partikeltypen
        if type1 != type2:  # Normalerweise ist Anziehung zwischen verschiedenen Typen
            self.interactions[(type1, type2)][2] = strength
            self.interactions[(type2, type1)][2] = strength  # Symmetrische Interaktion

    def calculate_force(self, p1: Particle, p2: Particle):
        force, radius, attraction = self.interactions[p1.type, p2.type]
        distance = self._distance(p1.position, p2.position)

        if distance <= radius:
            applied_force = (force / distance ** 2) - attraction  # Anziehende Kraft anwenden
            x_force = (p2.position[0] - p1.position[0]) * applied_force
            y_force = (p2.position[1] - p1.position[1]) * applied_force
            return x_force, y_force
        return 0, 0

    @staticmethod
    def _distance(p1_pos, p2_pos):
        return ((p2_pos[0] - p1_pos[0]) ** 2 + (p2_pos[1] - p1_pos[1]) ** 2) ** 0.5


# tests/test_interaction_matrix.py
import pytest
from src.interaction_matrix import InteractionMatrix
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


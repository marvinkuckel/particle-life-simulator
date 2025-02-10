import random
from math import sqrt

class InteractionMatrix:
    def __init__(self, num_types: int, default_radius: float):
        self.default_radius = default_radius
        # Erstellen der Interaktionsmatrix
        self.interactions = {
            force = random.choice((1, -1)) * random.choice((0, 0.2, 0.4, 0.6, 0.8, 1))
            (i, j): [force, self.default_radius, 1.0]  # Default strength is 1.0 (no attraction)
            for i in range(num_types) for j in range(num_types)
        }

    def add_attraction(self, type1, type2, strength):
        # Setzt eine Anziehungswirkung zwischen zwei Partikeltypen
        if type1 != type2:  # Normalerweise ist Anziehung zwischen verschiedenen Typen
            self.interactions[(type1, type2)][2] = strength
            self.interactions[(type2, type1)][2] = strength  # Symmetrische Interaktion

    def calculate_force(self, p1, p2):
        force, radius, attraction = self.interactions[p1.type, p2.type]
        distance = self._distance(p1.position, p2.position)
        
        epsilon = 1e-6  # Kleine Zahl, um Division durch Null zu vermeiden
        if distance <= radius and distance > epsilon:
            applied_force = (force / (distance ** 2 + epsilon)) - attraction  # Anziehende Kraft anwenden
            x_force = (p2.position[0] - p1.position[0]) * applied_force
            y_force = (p2.position[1] - p1.position[1]) * applied_force
            return x_force, y_force
        return 0, 0
    
    @staticmethod
    def _distance(pos1, pos2):
        return sqrt((pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2)
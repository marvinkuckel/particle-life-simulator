from typing import Dict

from particle import Particle

class InteractionMatrix:
    matrix: dict[(int, int), float]
    
    def __init__(self, number_of_types: int, interaction_radius: float):
        self.default_interaction_radius = interaction_radius
        self.matrix = dict()
        for i in range(number_of_types):
            for j in range(number_of_types):
                self.matrix[i, j] = [0, interaction_radius]  # force, radius

    def calculate_force(self, p1: Particle, p2: Particle):
        if p1 is not p2:
            interaction = self.matrix[p1.type, p2.type]
            distance = self._distance(p1, p2)
            
            if distance < interaction[1]:  # d < interaction_radius
                x_force = (p2.x - p1.x) / distance**2 * interaction[0]
                y_force = (p2.y - p1.y) / distance**2 * interaction[0]
                return x_force, y_force
            
    def _distance(self, p1: Particle, p2: Particle):
        return ((p1.x - p2.x)**2 + (p1.y - p2.y)**2)**0.5
    
    def _add_type(self):
        current_number_of_types = max(self.matrix.keys())[0] + 1
        for i in range(current_number_of_types):
            self.matrix[i, current_number_of_types] = [0, self.default_interaction_radius]
            
    def _remove_type(self):
        highest_type_index = max(self.matrix.keys())[0]
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix)):
                if highest_type_index in (i, j):
                    del self.matrix[i, j]

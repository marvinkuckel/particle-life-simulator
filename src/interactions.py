from typing import Dict
from particle import Particle

class InteractionMatrix:
    matrix: dict[(int, int), float]

    def __init__(self, number_of_types: int, interaction_radius: float):
        self.default_interaction_radius = interaction_radius
        self.matrix = {}
        for i in range(number_of_types):
            for j in range(number_of_types):
                self.matrix[i, j] = [0, interaction_radius]  # force, radius

    def calculate_force(self, p1: Particle, p2: Particle):
        if p1 is not p2:
            interaction = self.matrix[p1.type, p2.type]
            dx = p2.x - p1.x
            dy = p2.y - p1.y
            distance_sq = dx**2 + dy**2
            
            if distance_sq < interaction[1]**2:  # d < interaction_radius
                inv_distance_sq = interaction[0] / distance_sq
                x_force = dx * inv_distance_sq
                y_force = dy * inv_distance_sq
                return x_force, y_force

    def _add_type(self):
        current_number_of_types = max(self.matrix.keys())[0] + 1
        for i in range(current_number_of_types):
            self.matrix[i, current_number_of_types] = [0, self.default_interaction_radius]
            self.matrix[current_number_of_types, i] = [0, self.default_interaction_radius] # symmetric matrix

    def _remove_type(self):
        highest_type_index = max(self.matrix.keys())[0]
        to_remove = [key for key in list(self.matrix.keys()) if highest_type_index in key]
        for key in to_remove:
            del self.matrix[key]
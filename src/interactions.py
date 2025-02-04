import random

from particle import Particle

class InteractionMatrix:
    interactions: dict[(int, int), float]

    def __init__(self, number_of_types: int, default_interaction_radius: float):
        self.number_of_types = number_of_types
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

    # def _add_type(self):
    #     current_number_of_types = max(self.interactions.keys())[0] + 1
    #     for i in range(current_number_of_types):
    #         self.interactions[i, current_number_of_types] = [0, self.default_interaction_radius]
    #         self.interactions[current_number_of_types, i] = [0, self.default_interaction_radius] # symmetric matrix

    # def _remove_type(self):
    #     highest_type_index = max(self.interactions.keys())[0]
    #     to_remove = [key for key in list(self.interactions.keys()) if highest_type_index in key]
    #     for key in to_remove:
    #         del self.interactions[key]
import random
from math import sqrt


class InteractionMatrix:
    def __init__(self, num_types: int, min_radius: float, max_radius: float):
        self.number_of_types = num_types
        self.min_radius = min_radius  # shortest distance at which particles interact
        self.max_radius = max_radius  # farthest distance at which particles interact

        # random choice of either positive (attraction) or negative (repulsion) force between type pairs
        choice = lambda: random.choice((1, -1)) * random.choice((0, 0.2, 0.4, 0.6, 0.8, 1))
        # dictionary which stores type pairs & their interaction force 
        self.interactions = {
            (i, j): [choice()]  
            for i in range(num_types) for j in range(num_types)
        }
        
            
    def calculate_force(self, p1, p2):
        force_strength = self.interactions[p1.type, p2.type]
        distance = self._distance(p1.position, p2.position)
        epsilon = 1e-12   # small value to prevent division by zero
        
        # computes direction of the particles force vector
        direction_x = (p2.position[0] - p1.position[0]) / (distance + epsilon)
        direction_y = (p2.position[1] - p1.position[1]) / (distance + epsilon)
        
        
    @staticmethod
    # calculates distance between two particles
    def _distance(pos1, pos2):
        return sqrt((pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2)
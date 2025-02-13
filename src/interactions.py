import random
from math import sqrt


class InteractionMatrix:
    def __init__(self, num_types: int, min_radius: float, max_radius: float, global_repulsion: float):
        self.number_of_types = num_types
        self.min_radius = min_radius                # shortest distance at which particles interact
        self.max_radius = max_radius                # farthest distance at which particles interact
        self.global_repulsion = global_repulsion     # repulsive force between all particles to prevent overlap

        # random choice of either positive (attraction) or negative (repulsion) force between type pairs
        choice = lambda: random.choice((1, -1)) * random.choice((0, 0.2, 0.4, 0.6, 0.8, 1))
        # dictionary which stores type pairs & their interaction force 
        self.interactions = {
            (i, j): [choice()]  
            for i in range(num_types) for j in range(num_types)
        }
        
            
    def calculate_force(self, p1, p2):
        force_strength = self.interactions[p1.type, p2.type][0]
        distance = self._distance(p1.position, p2.position)
        epsilon = 1e-12   # small value to prevent division by zero
        
        # computes normalized direction vector
        direction_x = (p2.position[0] - p1.position[0]) / (distance + epsilon)
        direction_y = (p2.position[1] - p1.position[1]) / (distance + epsilon)

        # repulsion applies at all distances, but increases with smaller distance
        repulsion_strength = self.global_repulsion / (distance + epsilon)  
        x_repulsion = -direction_x * repulsion_strength
        y_repulsion = -direction_y * repulsion_strength

        # beyond the max_radius only global_repulsion, but no interaction force is applied
        if distance > self.max_radius:
            return x_repulsion, y_repulsion 
        
        # within interaction radius range interaction forces increase & decrease with proximity
        force_scale = (self.max_radius - distance) / (self.max_radius - self.min_radius)  
        net_force = force_strength * force_scale

        # combines direction, attraction and repulsion into force vector 
        x_force = direction_x * net_force + x_repulsion
        y_force = direction_y * net_force + y_repulsion

        return x_force, y_force
        
        
    @staticmethod
    # calculates distance between two particles
    def _distance(pos1, pos2):
        return sqrt((pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2)
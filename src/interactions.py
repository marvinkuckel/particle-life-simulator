import random
from math import sqrt
from numba import njit
import numpy as np


class InteractionMatrix:
    def __init__(self, num_types: int, min_radius: float, max_radius: float, global_repulsion: float):
        self.number_of_types = num_types
        self.min_radius = min_radius                # shortest distance at which particles interact
        self.max_radius = max_radius                # farthest distance at which particles interact
        self.global_repulsion = global_repulsion     # repulsive force between all particles to prevent overlap

        # numpay array which stores type pairs & their interaction force 
        self.interactions = np.zeros((num_types, num_types), dtype=np.float64)
        for i in range(num_types):
            for j in range(num_types):
                self.interactions[i, j] = random.choice((1, -1)) * random.choice((0, 0.2, 0.4, 0.6, 0.8, 1))
        
@njit            
def calculate_force(px1: float, py1: float, type1: int, 
                     px2: float, py2: float, type2: int, 
                     interactions: np.ndarray, global_repulsion: float, 
                     max_radius: float, min_radius: float,
                     max_repulsion: float = 5.0):
    force_strength = interactions[type1, type2]
    distance = _distance(px1, py1, px2, py2)
    epsilon = 1e-12   # small value to prevent division by zero
    
    # computes normalized direction vector
    direction_x = (px2 - px1) / (distance + epsilon)
    direction_y = (py2 - py1) / (distance + epsilon)

    # repulsion applies at all distances, but increases with smaller distance
    repulsion_strength = global_repulsion / (distance + epsilon)  

    # cap repulsion to prevent particles from bursting apart too much
    repulsion_strength = min(repulsion_strength, max_repulsion)  
    
    x_repulsion = -direction_x * repulsion_strength
    y_repulsion = -direction_y * repulsion_strength

    # beyond the max_radius only global_repulsion, but no interaction force is applied
    if distance > max_radius:
        return x_repulsion, y_repulsion 
    
    # within interaction radius range interaction forces increase & decrease with proximity
    force_scale = (max_radius - distance) / (max_radius - min_radius)  
    net_force = force_strength * force_scale

    # combines direction, attraction and repulsion into force vector 
    x_force = direction_x * net_force + x_repulsion
    y_force = direction_y * net_force + y_repulsion

    return x_force, y_force
        
        
@njit
# calculates distance between two particles
def _distance(px1, py1, px2, py2):
    return sqrt((px2 - px1) ** 2 + (py2 - py1) ** 2)
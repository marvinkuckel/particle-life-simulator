import random
from math import sqrt
from numba import njit
import numpy as np

class InteractionMatrix:
    def __init__(self, num_types: int, min_radius: float, max_radius: float, global_repulsion: float):
        """
        Creates a matrix of forces between particle types.
        num_types: Number of particle types.
        min_radius: Shortest distance at which particles interact.
        max_radius: Farthest distance at which particles interact.
        global_repulsion: Repulsive force between all particles to prevent overlap.
        """
        self.number_of_types = num_types
        self.min_radius = min_radius
        self.max_radius = max_radius
        self.global_repulsion = global_repulsion

        # Numpy array which stores type pairs & their interaction force 
        self.interactions = np.zeros((num_types, num_types), dtype=np.float64)  # Initialize matrix with zeros
        for i in range(num_types):
            for j in range(num_types):

                self.interactions[i, j] = random.choice((1, -1)) * random.choice((0, 0.2, 0.4, 0.6, 0.8, 1))
    
    def randomize_fields(self):
        for i in range(self.number_of_types):
            for j in range(self.number_of_types):
                self.interactions[i, j] = random.choice((1, -1)) * random.choice((0, 0.2, 0.4, 0.6, 0.8, 1))
    
    def set_min_radius(self, min_radius: float):
        self.min_radius = min_radius
        
    def get_min_radius(self):
        return self.min_radius
        
    def set_max_radius(self, max_radius: float):
        self.max_radius = max_radius
        
    def get_max_radius(self):
        return self.max_radius
        
    def set_global_repulsion(self, global_repulsion: float):
        self.global_repulsion = global_repulsion
        
    def get_global_repulsion(self):
        return self.global_repulsion
        
        
@njit            
def calculate_force(px1: float, py1: float, type1: int, 
                     px2: float, py2: float, type2: int, 
                     interactions: np.ndarray, global_repulsion: float, 
                     max_radius: float, min_radius: float,
                     max_repulsion: float = 5.0):

    force_strength = interactions[type1, type2]
    distance = _distance(px1, py1, px2, py2)
    epsilon = 1e-12  # Small value to prevent division by zero
    
    # Computes normalized direction vector between two particles
    # This is crucial because we only need the direction of the force, not the distance.
    direction_x = (px2 - px1) / (distance + epsilon)
    direction_y = (py2 - py1) / (distance + epsilon)

    # Repulsion applies at all distances, but increases with smaller distance
    repulsion_strength = global_repulsion / (distance + epsilon)  

    # cap repulsion to prevent particles from bursting apart too much
    repulsion_strength = min(repulsion_strength, max_repulsion)  
    
    x_repulsion = -direction_x * repulsion_strength
    y_repulsion = -direction_y * repulsion_strength

    # Beyond the max_radius only global_repulsion, but no interaction force is applied
    if distance > max_radius:  # If the distance is greater than the maximum interaction radius...
        return x_repulsion, y_repulsion  # ... only return the repulsion force (no interaction force applied)
    
    # Within interaction radius range interaction forces increase & decrease with proximity
    force_scale = (max_radius - distance) / (max_radius - min_radius)  
    net_force = force_strength * force_scale

    # Combines direction, attraction and repulsion into force vector 
    x_force = direction_x * net_force + x_repulsion
    y_force = direction_y * net_force + y_repulsion
    return x_force, y_force  # Returns the components of the force vector
        
@njit
# Calculates distance between two particles
def _distance(px1, py1, px2, py2):
    """
    Calculates the Euclidean distance between two particles
    using Numba for JIT compilation.
    """
    return sqrt((px2 - px1) ** 2 + (py2 - py1) ** 2)  # Euclid distance

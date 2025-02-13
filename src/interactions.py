import random
from math import sqrt

class InteractionMatrix:
    def __init__(self, num_types: int, default_radius: float):
        self.number_of_types = num_types
        self.default_radius = default_radius
        choice = lambda: random.choice((1, -1)) * random.choice((0, 0.2, 0.4, 0.6, 0.8, 1))
        
        # Erstellen der Interaktionsmatrix
        self.interactions = {
            (i, j): [choice(), self.default_radius]  
            for i in range(num_types) for j in range(num_types)
        }
        #self.min_distance = 0.05  #minimum allowed distance between particles (prevents touching & sticking)
        #self.smooth_factor = 0.05  #strength of the smooth force reduction
            
    def calculate_force(self, p1, p2):
        force_streng, radius = self.interactions[p1.type, p2.type]
        
        # Skip calculation if force strength is zero (no interaction) to safe time
        if force_streng == 0:
            return 0, 0
        
        distance = self._distance(p1.position, p2.position)
        min_distance = 0.02 
        epsilon = 1e-12   #small value to prevent division by zero or the programm crashes
        
        #compute direction and normalize the force vector
        direction_x = (p2.position[0] - p1.position[0]) / (distance + epsilon)
        direction_y = (p2.position[1] - p1.position[1]) / (distance + epsilon)
        
        # Soft transition near min_distance to avoid the glitching problem
        if distance < min_distance:
            repulsion_strength = (min_distance / (distance + epsilon)) ** 2  # Quadratic scaling for smooth repulsion
            return direction_x * repulsion_strength, direction_y * repulsion_strength  

    
        if distance <= radius and distance > epsilon:
                applied_force = (force_streng / (distance ** 2 + epsilon))  # Anziehende Kraft anwenden
                x_force = (p2.position[0] - p1.position[0]) * applied_force
                y_force = (p2.position[1] - p1.position[1]) * applied_force
                return x_force, y_force
        return 0, 0
    
    @staticmethod
    def _distance(pos1, pos2):
        return sqrt((pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2)
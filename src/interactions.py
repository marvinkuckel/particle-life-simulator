import random
from math import sqrt

class InteractionMatrix:
    def __init__(self, num_types: int, default_radius: float):
        self.number_of_types = num_types
        self.default_radius = default_radius
        choice = lambda: random.choice((1, -1)) * random.choice((0, 0.2, 0.4, 0.6, 0.8, 1))
        
        # Erstellen der Interaktionsmatrix
        self.interactions = {
            (i, j): [choice(), self.default_radius, 1.0]  # Default strength is 1.0 (no attraction)
            for i in range(num_types) for j in range(num_types)
        }
        self.min_distance = 0.05  #minimum allowed distance between particles (prevents touching & sticking)
        self.smooth_factor = 0.05  #strength of the smooth force reduction

    def add_attraction(self, type1, type2, strength):
        #Set an attraction force between two particle types.
        #The interaction is symmetric, meaning the attraction applies in both directions.
        if type1 != type2:
            self.interactions[(type1, type2)][2] = strength
            self.interactions[(type2, type1)][2] = strength 
            
    def calculate_force(self, p1, p2):
        force_streng, radius, attraction = self.interactions[p1.type, p2.type]
        
        # Skip calculation if force strength is zero (no interaction) to safe time
        if force_streng == 0:
            return 0, 0
        
        distance = self._distance(p1.position, p2.position)
        
        epsilon = 1e-10   #small value to prevent division by zero or the programm crashes
        
        #compute direction and normalize the force vector
        direction_x = (p2.position[0] - p1.position[0]) / (distance + epsilon)
        direction_y = (p2.position[1] - p1.position[1]) / (distance + epsilon)
            
        # Soft transition near min_distance to avoid the glitching problem
        if distance < self.min_distance:
            # Reduce force smoothly when close to the min_distance
            scale = (distance / self.min_distance) ** 2  # quadrat scaling for smooth transition
            return direction_x * scale, direction_y * scale  


        if distance <= radius:
            applied_force = force_streng / (distance ** 2 + self.smooth_factor) - attraction    
            return direction_x * applied_force, direction_y * applied_force
        return 0, 0 #no force if partikles are beyond the interaction rafius
    
    @staticmethod
    def _distance(pos1, pos2):
        return sqrt((pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2)
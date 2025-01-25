# interaction_matrix.py
import random
from particle import Particle


class InteractionMatrix:
    def __init__(self, num_types: int, default_radius: float):
        self.default_radius = default_radius
        # Erstellen der Interaktionsmatrix
        self.interactions = {
            (i, j): [random.choice((1, -1)) * 0.5, self.default_radius, 1.0]  # Default strength is 1.0 (no attraction)
            for i in range(num_types) for j in range(num_types)
        }

    def add_attraction(self, type1, type2, strength):
        # Setzt eine Anziehungswirkung zwischen zwei Partikeltypen
        if type1 != type2:  # Normalerweise ist Anziehung zwischen verschiedenen Typen
            self.interactions[(type1, type2)][2] = strength
            self.interactions[(type2, type1)][2] = strength  # Symmetrische Interaktion

    def calculate_force(self, p1: Particle, p2: Particle):
        force, radius, attraction = self.interactions[p1.type, p2.type]
        distance = self._distance(p1.position, p2.position)

        if distance <= radius:
            if distance > 0.005:  # Verhindert Division durch zu kleine Distanz
                applied_force = (force / distance ** 2) - attraction
                x_force = (p2.position[0] - p1.position[0]) * applied_force
                y_force = (p2.position[1] - p1.position[1]) * applied_force
            else:
                applied_force = 1 / ((distance + 0.000001) ** distance)
                x_force = -(p2.position[0] - p1.position[0]) * applied_force
                y_force = -(p2.position[1] - p1.position[1]) * applied_force

            # Debug-Ausgabe
            print(f"DEBUG: force={force}, radius={radius}, attraction={attraction}, "
                  f"distance={distance}, applied_force={applied_force}, "
                  f"x_force={x_force}, y_force={y_force}")
            return x_force, y_force
        return 0, 0

    @staticmethod
    def _distance(p1_pos, p2_pos):
        return ((p2_pos[0] - p1_pos[0])**2 + (p2_pos[1] - p1_pos[1])**2) ** 0.5

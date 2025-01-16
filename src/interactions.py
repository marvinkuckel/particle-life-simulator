import random

from particle import Particle

class InteractionMatrix:
    def __init__(self, num_types: int, default_radius: float, attraction_strength: float = 0.01):
        self.default_radius = default_radius
        self.attraction_strength = attraction_strength  # Stärke der Anziehungskraft
        self.interactions = {
            (i, j): [random.choice((1, -1)) * 0.5, self.default_radius]
            for i in range(num_types) for j in range(num_types)
        }

    def calculate_force(self, p1, p2):
        # Berechnet die Anziehungskraft oder Abstoßung zwischen den Partikeln
        force, radius = self.interactions[p1.type, p2.type]
        distance = self._distance(p1.position, p2.position)
        
        if distance <= radius and distance > 0.005:
            # Anziehungskraft Berechnung (vereinfachtes Gravitationsgesetz)
            # G * m1 * m2 / r^2 - hier verwenden wir die `size` als `m1` und `m2` und einen konstanten Anziehungsfaktor.
            attraction_force = self.attraction_strength * p1.size * p2.size / (distance ** 2)
            
            # Anziehungskraft wird auf den Abstand angewendet
            applied_force = force + attraction_force
            
            # Berechnet die Richtung der Kraft basierend auf dem Abstand
            x_force = (p2.position[0] - p1.position[0]) * applied_force
            y_force = (p2.position[1] - p1.position[1]) * applied_force
            return x_force, y_force
        
        return 0, 0

    @staticmethod
    def _distance(p1_pos, p2_pos):
        return ((p2_pos[0] - p1_pos[0]) ** 2 + (p2_pos[1] - p1_pos[1]) ** 2) ** 0.5

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
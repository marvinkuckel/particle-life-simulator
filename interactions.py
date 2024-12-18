from typing import Dict
from particle import Particle

class InteractionMatrix:
    matrix: dict[(int, int), float]

    def __init__(self, number_of_types: int, interaction_radius: float, display_width: float = None, display_height: float = None):
        self.default_interaction_radius = interaction_radius
        self.matrix = {}
        self.display_width = display_width
        self.display_height = display_height
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

    def _distance(self, p1: Particle, p2: Particle):
        return ((p1.x - p2.x)**2 + (p1.y - p2.y)**2)**0.5

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

    def apply_border_collision(self, p: Particle):
        """Prüft, ob das Partikel den Rand des Displays erreicht hat und sorgt für Abprallen."""
        if p.x <= 0 or p.x >= self.display_width:  # Überprüft die X-Achse
            p.vx *= -1  # Geschwindigkeit in X-Richtung umkehren
        if p.y <= 0 or p.y >= self.display_height:  # Überprüft die Y-Achse
            p.vy *= -1  # Geschwindigkeit in Y-Richtung umkehren

    def apply_attraction(self, p1: Particle, p2: Particle, attraction_strength: float):
        """Berechnet die Anziehungskraft zwischen zwei Partikeln."""
        distance = self._distance(p1, p2)
        if distance < 100:  # Beispiel: nur Anziehung wenn Partikel nahe genug sind
            force = attraction_strength / distance**2
            # Anziehungskraft in Richtung des anderen Partikels anwenden
            fx = (p2.x - p1.x) * force
            fy = (p2.y - p1.y) * force
            return fx, fy
        return 0, 0

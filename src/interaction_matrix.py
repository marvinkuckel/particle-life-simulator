import random
from src.particle import Particle  # Annahme: Particle ist in src/particle.py definiert

class InteractionMatrix:
    def __init__(self, num_types: int, default_radius: float):
        """
        Initialisiert die Interaktionsmatrix mit zufälligen Kräften und Standardradius.
        
        :param num_types: Anzahl der verschiedenen Partikeltypen.
        :param default_radius: Standardradius der Interaktion zwischen Partikeln.
        """
        self.default_radius = default_radius
        # Initialisiere die Interaktionen für alle möglichen Typenpaare
        self.interactions = {
            (i, j): [random.choice((1, -1)) * 0.5, self.default_radius, 1.0]  # Standardstärke: 1.0
            for i in range(num_types) for j in range(num_types)
        }

    def add_attraction(self, type1: int, type2: int, strength: float):
        """
        Setzt eine Anziehungskraft zwischen zwei Partikeltypen.
        
        :param type1: Typ des ersten Partikels.
        :param type2: Typ des zweiten Partikels.
        :param strength: Stärke der Anziehungskraft.
        """
        if type1 != type2:  # Anziehung normalerweise nur zwischen verschiedenen Typen
            self.interactions[(type1, type2)][2] = strength
            self.interactions[(type2, type1)][2] = strength  # Symmetrisch

    def calculate_force(self, p1: Particle, p2: Particle):
        """
        Berechnet die Kraft zwischen zwei Partikeln basierend auf ihrer Typen-Interaktion.
        
        :param p1: Erstes Partikel.
        :param p2: Zweites Partikel.
        :return: Kraft in x- und y-Richtung als Tuple (x_force, y_force).
        """
        force, radius, attraction = self.interactions[(p1.type, p2.type)]
        distance = self._distance(p1.position, p2.position)

        if distance <= radius:
            applied_force = (force / distance ** 2) - attraction  # Attraction und Repulsion kombinieren
            x_force = (p2.position[0] - p1.position[0]) * applied_force
            y_force = (p2.position[1] - p1.position[1]) * applied_force
            return x_force, y_force
        return 0, 0

    @staticmethod
    def _distance(p1_pos, p2_pos):
        """
        Berechnet die euklidische Distanz zwischen zwei Punkten.
        
        :param p1_pos: Position des ersten Punktes (x, y).
        :param p2_pos: Position des zweiten Punktes (x, y).
        :return: Euklidische Distanz.
        """
        return ((p2_pos[0] - p1_pos[0]) ** 2 + (p2_pos[1] - p1_pos[1]) ** 2) ** 0.5


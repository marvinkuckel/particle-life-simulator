# test_interaction_matrix.py

import pytest
from src.interactions import InteractionMatrix
from src.particle import Particle
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))


def test_calculate_force_no_interaction():
    interaction_matrix = InteractionMatrix(num_types=4, max_radius=0.09, min_radius=0, global_repulsion=0)
    interaction_matrix.interactions[(0, 1)] = [1]
    p1 = Particle(type=0, size=2, position=(0.1, 0.1))
    p2 = Particle(type=1, size=2, position=(0.1, 0.2))
    
    # Keine Wechselwirkung, wenn die Distanzen zu groß sind
    force_x, force_y = interaction_matrix.calculate_force(p1, p2)
    print(f"DEBUG: force_x={force_x}, force_y={force_y}")  # Debugging-Ausgabe
    assert force_x == 0
    assert force_y == 0

def test_calculate_force_with_interaction():
    interaction_matrix = InteractionMatrix(num_types=4, max_radius=0.5, min_radius=0, global_repulsion=0)
    interaction_matrix.interactions[(0, 1)] = [0.1]
    p1 = Particle(type=0, size=2, position=(0.1, 0.1))
    p2 = Particle(type=1, size=2, position=(0.1, 0.15))
    
    # Test: Wechselwirkung, wenn die Distanz klein genug ist
    force_x, force_y = interaction_matrix.calculate_force(p1, p2)
    print(f"DEBUG: force_x={force_x}, force_y={force_y}")  # Debugging-Ausgabe
    
    # Überprüfen, ob die Kraft signifikant ist (mit einer Toleranz für sehr kleine Kräfte)
    threshold = 1e-12  # Toleranz
    assert abs(force_x) > threshold or abs(force_y) > threshold, f"Kräfte sind zu klein: force_x={force_x}, force_y={force_y}"




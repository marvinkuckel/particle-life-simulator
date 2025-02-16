import pytest
from src.interactions import InteractionMatrix, calculate_force
from src.particle import Particle
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

def test_calculate_force_no_interaction():
    # Create an InteractionMatrix with no interaction
    interaction_matrix = InteractionMatrix(num_types=4, max_radius=0.09, min_radius=0, global_repulsion=0)
    interaction_matrix.interactions[(0, 1)] = 1  # Set interaction value as a scalar instead of a list
    p1 = Particle(type=0, size=2, position=[0.1, 0.1])
    p2 = Particle(type=1, size=2, position=[0.1, 0.2])
    
    # No interaction when the distance is too large
    force_x, force_y = calculate_force(p1.position[0], p1.position[1], p1.type, p2.position[0], p2.position[1], p2.type,
                                       interaction_matrix.interactions, interaction_matrix.global_repulsion,
                                       interaction_matrix.max_radius, interaction_matrix.min_radius)
    print(f"DEBUG: force_x={force_x}, force_y={force_y}")  # Debugging output
    assert force_x == 0
    assert force_y == 0

def test_calculate_force_with_interaction():
    # Create InteractionMatrix with interaction
    interaction_matrix = InteractionMatrix(num_types=4, max_radius=0.5, min_radius=0, global_repulsion=0)
    interaction_matrix.interactions[(0, 1)] = 0.1  # Set interaction value as a scalar instead of a list
    p1 = Particle(type=0, size=2, position=[0.1, 0.1])
    p2 = Particle(type=1, size=2, position=[0.1, 0.15])
    
    # Test: Interaction when distance is small enough
    force_x, force_y = calculate_force(p1.position[0], p1.position[1], p1.type, p2.position[0], p2.position[1], p2.type,
                                       interaction_matrix.interactions, interaction_matrix.global_repulsion,
                                       interaction_matrix.max_radius, interaction_matrix.min_radius)
    print(f"DEBUG: force_x={force_x}, force_y={force_y}")  # Debugging output
    
    # Check if the force is significant (with a tolerance for very small forces)
    threshold = 1e-12  # Tolerance
    assert abs(force_x) > threshold or abs(force_y) > threshold, f"Forces are too small: force_x={force_x}, force_y={force_y}"

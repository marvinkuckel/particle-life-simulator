import sys
import os
import unittest
import numpy as np


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# Debugging
print("Aktueller sys.path:")
print(sys.path)

from interactions import InteractionMatrix, calculate_force

class TestParticleSimulation(unittest.TestCase):

    def test_interaction_matrix_initialization(self):
        # Test Interaktionsmatrix 
        matrix = InteractionMatrix(3, 0.5, 2.0, 0.1)
        self.assertEqual(matrix.interactions.shape, (3, 3))  # Testet, ob die Matrix die richtige Größe hat

    def test_calculate_force(self):
        # Test calculate_force
        interactions = np.array([[0.0, 0.5, -0.2], [0.5, 0.0, 0.3], [-0.2, 0.3, 0.0]])
        force_x, force_y = calculate_force(0.0, 0.0, 0, 1.0, 1.0, 1, interactions, 0.1, 2.0, 0.5)
        
        # Test Floats 
        self.assertIsInstance(force_x, float)
        self.assertIsInstance(force_y, float)

if __name__ == "__main__":
    unittest.main()



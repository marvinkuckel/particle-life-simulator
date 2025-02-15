import sys
import os
import unittest
import numpy as np

# Füge das 'src'-Verzeichnis zum Python-Pfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# Debugging: Überprüfen, ob der Pfad korrekt hinzugefügt wurde
print("Aktueller sys.path:")
print(sys.path)

# Importiere die Funktionen und Klassen aus interactions.py
from interactions import InteractionMatrix, calculate_force

class TestParticleSimulation(unittest.TestCase):

    def test_interaction_matrix_initialization(self):
        # Testet, ob die Interaktionsmatrix richtig initialisiert wurde
        matrix = InteractionMatrix(3, 0.5, 2.0, 0.1)
        self.assertEqual(matrix.interactions.shape, (3, 3))  # Testet, ob die Matrix die richtige Größe hat

    def test_calculate_force(self):
        # Testet die Funktion calculate_force
        interactions = np.array([[0.0, 0.5, -0.2], [0.5, 0.0, 0.3], [-0.2, 0.3, 0.0]])
        force_x, force_y = calculate_force(0.0, 0.0, 0, 1.0, 1.0, 1, interactions, 0.1, 2.0, 0.5)
        
        # Testet, ob die Rückgabewerte Floats sind
        self.assertIsInstance(force_x, float)
        self.assertIsInstance(force_y, float)

if __name__ == "__main__":
    unittest.main()



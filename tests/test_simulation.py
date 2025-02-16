import unittest
import numpy as np
from particle import Particle
from interactions import InteractionMatrix, calculate_force
from simulation import Simulation
import sys
sys.path.insert(0, 'src')
from particle import Particle


class TestSimulation(unittest.TestCase):

    def setUp(self):
        # Setup, um zu Beginn jedes Tests eine frische Simulation zu erstellen
        self.interaction_matrix = InteractionMatrix(num_types=4, min_radius=0.1, max_radius=0.5, global_repulsion=0.05)
        self.simulation = Simulation(width=100, height=100, interaction_matrix=self.interaction_matrix, num_particles=10)

    def test_initialization(self):
        # Testet, ob die Simulation korrekt initialisiert wurde
        self.assertEqual(len(self.simulation.particles), 10)  # Teste, ob 10 Partikel erstellt wurden
        self.assertEqual(self.simulation.width, 100)          # Teste, ob die Breite korrekt gesetzt wurde
        self.assertEqual(self.simulation.height, 100)         # Teste, ob die Höhe korrekt gesetzt wurde

    def test_particle_positions(self):
        # Testet, ob Partikel an zufälligen Positionen erzeugt werden
        for particle in self.simulation.particles:
            self.assertTrue(0 <= particle.position[0] <= 1)  # Teste, ob x-Position im gültigen Bereich ist
            self.assertTrue(0 <= particle.position[1] <= 1)  # Teste, ob y-Position im gültigen Bereich ist

    def test_update(self):
        # Testet das Update der Simulation und die Position der Partikel nach einem Update
        initial_positions = [p.position.copy() for p in self.simulation.particles]
        self.simulation.update(dt=0.1)
        # Überprüfe, ob sich die Partikelpositionen geändert haben
        for i, particle in enumerate(self.simulation.particles):
            self.assertNotEqual(particle.position[0], initial_positions[i][0])  # x-Position sollte sich ändern
            self.assertNotEqual(particle.position[1], initial_positions[i][1])  # y-Position sollte sich ändern

    def test_enforce_boundaries(self):
        # Testet, ob die Begrenzungen korrekt durchgesetzt werden
        particle = Particle(position=(0.0, 0.0), velocity=(-1.0, -1.0), type=0, size=1, friction=0.5, random_movement=0.01)
        self.simulation.particles = np.array([particle])  # Setze einen Partikel in der Simulation
        self.simulation.enforce_boundaries()
        # Teste, ob der Partikel auf der anderen Seite des Rands wieder auftaucht
        self.assertGreaterEqual(particle.position[0], 0)  # x-Position sollte >= 0 sein
        self.assertLessEqual(particle.position[0], 1)     # x-Position sollte <= 1 sein
        self.assertGreaterEqual(particle.position[1], 0)  # y-Position sollte >= 0 sein
        self.assertLessEqual(particle.position[1], 1)     # y-Position sollte <= 1 sein

if __name__ == "__main__":
    unittest.main()

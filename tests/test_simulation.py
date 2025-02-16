import unittest
import numpy as np
import sys
sys.path.insert(0, 'src')  
from src.particle import Particle
from src.interactions import InteractionMatrix, calculate_force
from src.simulation import Simulation


class TestSimulation(unittest.TestCase):

    def setUp(self):
        # Setup to create a fresh simulation at the beginning of each test.
        self.interaction_matrix = InteractionMatrix(num_types=4, min_radius=0.1, max_radius=0.5, global_repulsion=0.05)
        self.simulation = Simulation(width=100, height=100, interaction_matrix=self.interaction_matrix, num_particles=10)

    def test_initialization(self):
        # Tests whether the simulation was initialized correctly.
        self.assertEqual(len(self.simulation.particles), 10)  
        self.assertEqual(self.simulation.width, 100)          
        self.assertEqual(self.simulation.height, 100)         

    def test_particle_positions(self):
        # Tests whether particles are generated at random positions.
        for particle in self.simulation.particles:
            self.assertTrue(0 <= particle.position[0] <= 1) 
            self.assertTrue(0 <= particle.position[1] <= 1)  

    def test_update(self):
        # Tests the simulation update and the position of the particles after an update.
        initial_positions = [p.position for p in self.simulation.particles]
        self.simulation.update(dt=0.1)
        # Check whether the particle positions have changed.
        for i, particle in enumerate(self.simulation.particles):
            self.assertNotEqual(particle.position[0], initial_positions[i][0])  
            self.assertNotEqual(particle.position[1], initial_positions[i][1])  

    def test_enforce_boundaries(self):
        # Tests whether the boundaries are enforced correctly.
        particle = Particle(position=[0.0, 0.0], velocity=[-1.0, -1.0], type=0, size=1, friction=0.5, random_movement=0.01)
        self.simulation.particles = np.array([particle])  
        self.simulation.enforce_boundaries()
        # Tests whether the particle reappears on the other side of the boundary.
        self.assertGreaterEqual(particle.position[0], 0)  # x-Position should be >= 0 sein
        self.assertLessEqual(particle.position[0], 1)     # x-Position should be <= 1 sein
        self.assertGreaterEqual(particle.position[1], 0)  # y-Position should be >= 0 sein
        self.assertLessEqual(particle.position[1], 1)     # y-Position should be <= 1 sein

if __name__ == "__main__":
    unittest.main()

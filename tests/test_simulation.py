import unittest
import numpy as np
import sys
sys.path.insert(0, 'src') 
from src.particle import Particle
from src.interactions import InteractionMatrix, calculate_force
from src.simulation import Simulation

class TestSimulation(unittest.TestCase):

    def setUp(self):
        # sets up a simulation with predefined parameters for each test
        self.interaction_matrix = InteractionMatrix(num_types=5, min_radius=0.01, max_radius=0.15, global_repulsion=0.005)
        self.simulation = Simulation(
            width=1000, 
            height=1000, 
            interaction_matrix=self.interaction_matrix, 
            num_particles=1000,
            num_types=5,  
            time_factor=0.1,  
            force_scaling=0.2,  
            friction=0.5,  
            random_movement=0.01  
        )

    def test_initialization(self):
        # verifies correct initialization of simulation settings and particle count
        self.assertEqual(len(self.simulation.particles), 1000)
        self.assertEqual(self.simulation.width, 1000)
        self.assertEqual(self.simulation.height, 1000)

    def test_particle_positions(self):
        # ensures all particles are initialized within the defined boundaries
        for particle in self.simulation.particles:
            self.assertTrue(0 <= particle.position[0] <= 1)
            self.assertTrue(0 <= particle.position[1] <= 1)

    def test_update(self):
        # check simulation update changes particle positions as expected
        initial_positions = [p.position for p in self.simulation.particles]
        self.simulation.update(dt=0.1)
        for i, particle in enumerate(self.simulation.particles):
            self.assertNotEqual(particle.position[0], initial_positions[i][0])
            self.assertNotEqual(particle.position[1], initial_positions[i][1])

    def test_enforce_boundaries(self):
        # checks particles at the edge are correctly constrained in simulation
        particle = Particle(position=[0.0, 0.0], velocity=[-1.0, -1.0], type=0, size=1, force_scaling=0.2, friction=0.5, random_movement=0.01)
        self.simulation.particles = np.array([particle])
        self.simulation.enforce_boundaries()
        self.assertGreaterEqual(particle.position[0], 0)
        self.assertLessEqual(particle.position[0], 1)
        self.assertGreaterEqual(particle.position[1], 0)
        self.assertLessEqual(particle.position[1], 1)

if __name__ == "__main__":
    unittest.main()

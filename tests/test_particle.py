import unittest
import pygame
import sys
sys.path.insert(0, 'src') 
from src.main import simulation_parameters
from src.particle import Particle

class TestParticle(unittest.TestCase):
    def setUp(self):
        # initialize pygame and set up a display
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        # initialize particle
        self.particle = Particle(
            type=1, 
            size=10, 
            position=[0.5, 0.5], 
            velocity=[0.1, 0.2], 
            friction=simulation_parameters['friction'],
            force_scaling=simulation_parameters['force_scaling'],
            random_movement=simulation_parameters['random_movement']
        )

    def test_initialization(self):
        # check if particle is initialized with correct attributes
        self.assertEqual(self.particle.type, 1)
        self.assertEqual(self.particle.size, 10)
        self.assertEqual(self.particle.position, [0.5, 0.5])
        self.assertEqual(self.particle.velocity, [0.1, 0.2])
        self.assertEqual(self.particle.friction, simulation_parameters['friction'])
        self.assertEqual(self.particle.force_scaling, simulation_parameters['force_scaling'])
        self.assertEqual(self.particle.random_movement, simulation_parameters['random_movement'])

    def test_apply_force(self):
        # verify that velocity changes after applying a force
        force_x, force_y = 0.5, -0.5
        expected_velocity_x = 0.1 + force_x * self.particle.force_scaling
        expected_velocity_y = 0.2 + force_y * self.particle.force_scaling
        self.particle.apply_force(force_x, force_y)
        self.assertAlmostEqual(self.particle.velocity[0], expected_velocity_x, places=2)
        self.assertAlmostEqual(self.particle.velocity[1], expected_velocity_y, places=2)

    def test_update_position(self):
        # ensure that updating the particle's position changes it in expected manner
        initial_position = self.particle.position[:]
        self.particle.update_position(1, 1)
        self.assertNotEqual(self.particle.position, initial_position)
        self.assertGreater(self.particle.position[0], initial_position[0])
        self.assertGreater(self.particle.position[1], initial_position[1])

    def test_update_position_with_friction(self):
        # checks that friction correctly slows down the particle
        initial_velocity = self.particle.velocity[:]
        self.particle.update_position(1, 1)
        self.assertLess(self.particle.velocity[0], initial_velocity[0])
        self.assertLess(self.particle.velocity[1], initial_velocity[1])

    def test_random_movement(self):
        # test if random movement alters the particles position
        initial_position = self.particle.position[:]
        self.particle.update_position(1, 1)
        self.assertNotEqual(self.particle.position, initial_position)
        self.assertTrue(abs(self.particle.position[0] - initial_position[0]) > 0)
        self.assertTrue(abs(self.particle.position[1] - initial_position[1]) > 0)

    def test_draw(self):
        # ensures particle can be drawn to the screen without errors
        try:
            self.particle.draw(self.screen, self.screen_width, self.screen_height, (255, 0, 0))
        except Exception as e:
            self.fail(f"draw raised {type(e)} unexpectedly!")

    def tearDown(self):
        # clean up by quitting pygame
        pygame.quit()

if __name__ == "__main__":
    unittest.main()

import unittest
import random
import pygame
from src.particle import Particle

class TestParticle(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        # Correctly initialize Particle with force_scaling parameter
        self.particle = Particle(type=1, size=10, position=[0.5, 0.5], velocity=[0.1, 0.2], friction=0.05, force_scaling=0.03, random_movement=0.1)

    def test_initialization(self):
        self.assertEqual(self.particle.type, 1)
        self.assertEqual(self.particle.size, 10)
        self.assertEqual(self.particle.position, [0.5, 0.5])
        self.assertEqual(self.particle.velocity, [0.1, 0.2])
        self.assertEqual(self.particle.friction, 0.05)
        self.assertEqual(self.particle.force_scaling, 0.03)  # Added test to check the force_scaling initialization
        self.assertEqual(self.particle.random_movement, 0.1)

    def test_apply_force(self):
        self.particle.apply_force(0.5, -0.5)
        self.assertAlmostEqual(self.particle.velocity[0], 0.1 + 0.5 * 0.03, places=2)
        self.assertAlmostEqual(self.particle.velocity[1], 0.2 - 0.5 * 0.03, places=2)

    def test_update_position(self):
        initial_position = self.particle.position.copy()
        self.particle.update_position(1, 1)
        self.assertNotEqual(self.particle.position, initial_position)
        self.assertGreater(self.particle.position[0], initial_position[0])
        self.assertGreater(self.particle.position[1], initial_position[1])

    def test_update_position_with_friction(self):
        initial_velocity = self.particle.velocity.copy()
        self.particle.update_position(1, 1)
        self.assertLess(self.particle.velocity[0], initial_velocity[0])
        self.assertLess(self.particle.velocity[1], initial_velocity[1])

    def test_random_movement(self):
        initial_position = self.particle.position.copy()
        self.particle.update_position(1, 1)
        self.assertNotEqual(self.particle.position, initial_position)
        self.assertTrue(abs(self.particle.position[0] - initial_position[0]) > 0)
        self.assertTrue(abs(self.particle.position[1] - initial_position[1]) > 0)

    def test_draw(self):
        try:
            self.particle.draw(self.screen, self.screen_width, self.screen_height, (255, 0, 0))
        except Exception as e:
            self.fail(f"draw raised {type(e)} unexpectedly!")

    def tearDown(self):
        pygame.quit()

if __name__ == "__main__":
    unittest.main()

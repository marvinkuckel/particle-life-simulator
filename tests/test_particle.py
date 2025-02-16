import unittest
import random
import pygame
from src.particle import Particle

class TestParticle(unittest.TestCase):
    def setUp(self):
        # Initialize Pygame
        pygame.init()
        
        # Screen dimensions for rendering
        self.screen_width = 800
        self.screen_height = 600
        
        # Create a screen to render particles
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        
        # Initialize a Particle object with the force_scaling parameter added
        self.particle = Particle(type=1, size=10, position=[0.5, 0.5], velocity=[0.1, 0.2], friction=0.05, force_scaling=0.03, random_movement=0.1)

    def test_initialization(self):
        # Test if the particle is initialized with the correct attributes
        self.assertEqual(self.particle.type, 1)
        self.assertEqual(self.particle.size, 10)
        self.assertEqual(self.particle.position, [0.5, 0.5])
        self.assertEqual(self.particle.velocity, [0.1, 0.2])
        self.assertEqual(self.particle.friction, 0.05)
        self.assertEqual(self.particle.random_movement, 0.1)
        self.assertEqual(self.particle.force_scaling, 0.03)  # Check the force_scaling value

    def test_apply_force(self):
        # Apply a force and check if the velocity is updated correctly considering the force_scaling
        self.particle.apply_force(0.5, -0.5)
        # force_scaling of 0.03 is used here
        self.assertAlmostEqual(self.particle.velocity[0], 0.1 + 0.5 * 0.03, places=2)
        self.assertAlmostEqual(self.particle.velocity[1], 0.2 - 0.5 * 0.03, places=2)

    def test_update_position(self):
        # Test if the position updates correctly
        initial_position = self.particle.position.copy()
        self.particle.update_position(1, 1)
        self.assertNotEqual(self.particle.position, initial_position)  # Check if position has changed
        self.assertGreater(self.particle.position[0], initial_position[0])  # Check if x has increased
        self.assertGreater(self.particle.position[1], initial_position[1])  # Check if y has increased

    def test_update_position_with_friction(self):
        # Test if friction is applied correctly, reducing the velocity
        initial_velocity = self.particle.velocity.copy()
        self.particle.update_position(1, 1)
        self.assertLess(self.particle.velocity[0], initial_velocity[0])  # Velocity should decrease due to friction
        self.assertLess(self.particle.velocity[1], initial_velocity[1])  # Same for the y-velocity

    def test_random_movement(self):
        # Test if random movement is applied correctly to the position
        initial_position = self.particle.position.copy()
        self.particle.update_position(1, 1)
        self.assertNotEqual(self.particle.position, initial_position)  # Check if position has changed
        self.assertTrue(abs(self.particle.position[0] - initial_position[0]) > 0)  # x-position should change
        self.assertTrue(abs(self.particle.position[1] - initial_position[1]) > 0)  # y-position should change

    def test_draw(self):
        # Test if the drawing function works without errors
        try:
            self.particle.draw(self.screen, self.screen_width, self.screen_height, (255, 0, 0))
        except Exception as e:
            self.fail(f"draw raised {type(e)} unexpectedly!")  # Fail the test if an exception is raised

    def tearDown(self):
        # Quit Pygame after the tests
        pygame.quit()

if __name__ == "__main__":
    unittest.main()

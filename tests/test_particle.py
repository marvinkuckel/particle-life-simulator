import unittest
from unittest.mock import MagicMock
import pygame
from src.particle import Particle

class TestParticle(unittest.TestCase):

    def setUp(self):
        # Setup: Creating a Particle object for the tests
        self.particle = Particle(
            type=1,
            size=10,
            position=(0.5, 0.5),
            velocity=(0.1, 0.2),
            friction=0.05,
            force_scaling=0.03,
            random_movement=0.1
        )
    
    def test_initialization(self):
        # Test if the particle is initialized correctly with the given parameters
        self.assertEqual(self.particle.type, 1)
        self.assertEqual(self.particle.size, 10)
        self.assertEqual(self.particle.position, (0.5, 0.5))
        self.assertEqual(self.particle.velocity, (0.1, 0.2))
        self.assertEqual(self.particle.friction, 0.05)
        self.assertEqual(self.particle.force_scaling, 0.03)
        self.assertEqual(self.particle.random_movement, 0.1)

    def test_apply_force(self):
        # Test if apply_force correctly modifies the particle's velocity
        self.particle.apply_force(0.5, -0.5)
        self.assertEqual(self.particle.velocity, [0.1 + 0.5 * 0.03, 0.2 - 0.5 * 0.03])

    def test_update_position(self):
        # Test if update_position correctly updates the particle's position
        initial_position = self.particle.position
        self.particle.update_position(dt=1, time_factor=1)
        # The position should change based on the velocity
        self.assertNotEqual(self.particle.position, initial_position)

    def test_random_movement(self):
        # Test if the random movement causes the position to change (within a small tolerance)
        initial_position = self.particle.position
        self.particle.update_position(dt=1, time_factor=1)
        self.assertNotEqual(self.particle.position, initial_position)
        # Check if the random movement has actually changed the position
        self.assertTrue(abs(self.particle.position[0] - initial_position[0]) > 0 or abs(self.particle.position[1] - initial_position[1]) > 0)

    def test_draw(self):
        # Test if the draw function is called and does not throw any errors
        pygame.init()
        screen = MagicMock()  # Create a mock object for the pygame screen
        self.particle.draw(screen, screen_width=800, screen_height=600, color=(255, 0, 0))

        # Ensure that the draw_circle method of pygame is called with the expected arguments
        screen.draw_circle.assert_called_once_with(screen, (255, 0, 0), (round(self.particle.position[0] * 800), round(self.particle.position[1] * 600)), 10)

    def tearDown(self):
        # Optional cleanup after tests
        pygame.quit()

if __name__ == '__main__':
    unittest.main()

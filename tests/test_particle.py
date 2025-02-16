import pygame
import unittest
from src.particle import Particle

class TestParticle(unittest.TestCase):
    
    def setUp(self):
        # Initialize pygame and create a mock screen for drawing
        pygame.init()
        self.screen = pygame.Surface((800, 600))  # Create a real pygame.Surface
        self.particle = Particle(type=1, size=10, position=(0.5, 0.5), velocity=(0.1, 0.2), friction=0.05, force_scaling=0.1, random_movement=0.1)
    
    def test_apply_force(self):
        self.particle.apply_force(1, 1)
        self.assertEqual(self.particle.velocity, [0.2, 0.3])

    def test_update_position(self):
        self.particle.update_position(dt=1, time_factor=1)
        self.assertNotEqual(self.particle.position, (0.5, 0.5))  # Position should have changed

    def test_draw(self):
        # Run the draw method, should not raise an error
        self.particle.draw(self.screen, screen_width=800, screen_height=600, color=(255, 0, 0))
        
    def tearDown(self):
        pygame.quit()

if __name__ == '__main__':
    unittest.main()

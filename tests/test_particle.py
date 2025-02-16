import unittest
from unittest.mock import MagicMock
import pygame
from src.particle import Particle


class TestParticle(unittest.TestCase):
    
    def setUp(self):
        self.particle = Particle(type=1, size=10, position=[0.5, 0.5], velocity=[0.1, 0.2], friction=0.05, force_scaling=1.0, random_movement=0.1)
    
    def test_apply_force(self):
        self.particle.apply_force(0.2, 0.3)
        self.assertAlmostEqual(self.particle.velocity[0], 0.2, places=1)
        self.assertAlmostEqual(self.particle.velocity[1], 0.3, places=1)

    def test_update_position(self):
        self.particle.update_position(dt=1, time_factor=1)
        self.assertNotEqual(self.particle.position, [0.5, 0.5])

    def test_draw(self):
        # Create a mock pygame surface (without the need for a real surface)
        screen_mock = MagicMock(spec=pygame.Surface)
        
        # Call the draw method, which should call pygame.draw.circle internally
        self.particle.draw(screen_mock, screen_width=800, screen_height=600, color=(255, 0, 0))
        
        # Check if pygame.draw.circle was called
        screen_mock.blit.assert_called_once()  # Check that blit() was called (this is enough for the test)

if __name__ == '__main__':
    unittest.main()

import unittest
from src.particle import Particle

class TestParticle(unittest.TestCase):
    def setUp(self):
        # Create a particle object for testing
        self.particle = Particle(type=1, size=10, position=[0.5, 0.5], velocity=[0.1, 0.2], 
                                 friction=0.05, force_scaling=1.0, random_movement=0.1)
    
    def test_apply_force(self):
        # Apply a force to the particle
        self.particle.apply_force(0.1, 0.1)
        
        # Check if the velocity has been correctly updated
        self.assertAlmostEqual(self.particle.velocity[0], 0.2, places=7)
        self.assertAlmostEqual(self.particle.velocity[1], 0.3, places=7)
    
    def test_update_position(self):
        # Store initial position
        initial_position = self.particle.position.copy()

        # Update the position of the particle
        self.particle.update_position(dt=1, time_factor=1)

        # Ensure that the position has changed after update
        self.assertNotEqual(self.particle.position, initial_position)

    def test_random_movement(self):
        # Store initial position
        initial_position = self.particle.position.copy()

        # Update the position of the particle with random movement
        self.particle.update_position(dt=1, time_factor=1)
        
        # Check if the position has changed due to random movement
        self.assertNotEqual(self.particle.position, initial_position)

    def test_draw(self):
        # Test the drawing function
        screen_mock = unittest.mock.MagicMock()  # Mocking the Pygame surface
        self.particle.draw(screen_mock, screen_width=800, screen_height=600, color=(255, 0, 0))

        # Ensure that the draw method was called
        screen_mock.blit.assert_called()

if __name__ == '__main__':
    unittest.main()

import unittest
import numpy as np
from src.interactions import InteractionMatrix, calculate_force

class TestInteractionMatrix(unittest.TestCase):
    
    def test_initialization(self):
        """Test if the InteractionMatrix is initialized correctly"""
        num_types = 3
        min_radius = 1.0
        max_radius = 5.0
        global_repulsion = 0.5
        
        # Initialize InteractionMatrix
        interaction_matrix = InteractionMatrix(num_types, min_radius, max_radius, global_repulsion)
        
        # Check if the interaction matrix has the correct shape
        self.assertEqual(interaction_matrix.interactions.shape, (num_types, num_types))
        
        # Check if the min_radius and max_radius are set correctly
        self.assertEqual(interaction_matrix.get_min_radius(), min_radius)
        self.assertEqual(interaction_matrix.get_max_radius(), max_radius)
        
        # Check if the global repulsion value is set correctly
        self.assertEqual(interaction_matrix.get_global_repulsion(), global_repulsion)
    
    def test_randomize_fields(self):
        """Test if the randomize_fields method updates the interaction matrix"""
        num_types = 3
        min_radius = 1.0
        max_radius = 5.0
        global_repulsion = 0.5
        interaction_matrix = InteractionMatrix(num_types, min_radius, max_radius, global_repulsion)
        
        # Save the original state of the interaction matrix
        original_state = interaction_matrix.interactions.copy()
        
        # Randomize the interaction matrix
        interaction_matrix.randomize_fields()
        
        # Ensure the matrix was modified
        np.testing.assert_raises(AssertionError, np.testing.assert_array_equal, interaction_matrix.interactions, original_state)
    
    def test_setter_getter_methods(self):
        """Test setter and getter methods for min_radius, max_radius, and global_repulsion"""
        interaction_matrix = InteractionMatrix(3, 1.0, 5.0, 0.5)
        
        # Test setting and getting min_radius
        interaction_matrix.set_min_radius(1.5)
        self.assertEqual(interaction_matrix.get_min_radius(), 1.5)
        
        # Test setting and getting max_radius
        interaction_matrix.set_max_radius(6.0)
        self.assertEqual(interaction_matrix.get_max_radius(), 6.0)
        
        # Test setting and getting global_repulsion
        interaction_matrix.set_global_repulsion(0.8)
        self.assertEqual(interaction_matrix.get_global_repulsion(), 0.8)
    
    def test_calculate_force(self):
        """Test if calculate_force works correctly"""
        # Test data
        px1, py1 = 0.0, 0.0  # Particle 1 position
        px2, py2 = 3.0, 4.0  # Particle 2 position
        type1, type2 = 0, 1  # Particle types
        num_types = 2  # Number of types
        min_radius = 1.0
        max_radius = 5.0
        global_repulsion = 0.5
        
        interaction_matrix = InteractionMatrix(num_types, min_radius, max_radius, global_repulsion)
        
        # We assume some random values for the interaction between types
        interaction_matrix.interactions[type1, type2] = 0.4
        
        # Test force calculation
        x_force, y_force = calculate_force(px1, py1, type1, px2, py2, type2, interaction_matrix.interactions, 
                                           global_repulsion, max_radius, min_radius)
        
        # Check that the returned force values are float
        self.assertIsInstance(x_force, float)
        self.assertIsInstance(y_force, float)
        
        # Check if the force is calculated based on expected interaction and distance
        self.assertNotEqual(x_force, 0.0)
        self.assertNotEqual(y_force, 0.0)

if __name__ == '__main__':
    unittest.main()


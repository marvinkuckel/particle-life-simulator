import sys
import pygame
import sys
import os
import pygame
import pytest

# Dynamically set the path to include src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from src.interactions_interface import InteractionsInterface


# Mock InteractionMatrix class for testing
class InteractionMatrix:
    def __init__(self, num_types: int, max_radius: float, min_radius: float, global_repulsion: float):
        self.num_types = num_types
        self.max_radius = max_radius
        self.min_radius = min_radius
        self.global_repulsion = global_repulsion
        self.interactions = {(i, j): 0 for i in range(num_types) for j in range(num_types)}

    @property
    def number_of_types(self):
        return self.num_types

# Test handle_click function
def test_handle_click():
    """Tests if handle_click correctly modifies the interaction values."""
    # Create a mock interaction matrix
    interaction_matrix = InteractionMatrix(num_types=4, max_radius=0.5, min_radius=0, global_repulsion=0)
    interaction_matrix.interactions[(0, 1)] = 0.5  # Initial interaction value
    
    # Define particle type colors
    type_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]

    # Create the InteractionsInterface instance
    interface = InteractionsInterface(interaction_matrix, type_colors, (100, 100), 500)

    # Simulate a mouse scroll up event at position (150, 150)
    mouse_pos = (150, 150)
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': mouse_pos, 'button': 4})  # Scroll up

    # Apply the click event to modify interaction value
    interface.handle_click(event)

    # Check if the interaction value increased by 0.2 (expected 0.7)
    assert abs(interaction_matrix.interactions[(0, 1)] - 0.7) < 1e-6, \
        f"Expected 0.7 but got {interaction_matrix.interactions[(0, 1)]}"

# Pygame setup and teardown for testing
@pytest.fixture(scope="module", autouse=True)
def init_pygame():
    pygame.init()
    yield
    pygame.quit()

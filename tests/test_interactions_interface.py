import pytest
import pygame
import sys
import os

# Dynamically set the path to include the src directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Import the InteractionsInterface class from the src directory
from src.interactions_interface import InteractionsInterface


# Mock InteractionMatrix class for testing purposes
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


# Testing the handle_click method
def test_handle_click():
    # Create a mock interaction matrix with 4 types
    interaction_matrix = InteractionMatrix(num_types=4, max_radius=0.5, min_radius=0, global_repulsion=0)
    interaction_matrix.interactions[(0, 1)] = 0.5  # Initial interaction value

    # Define particle type colors (for testing)
    type_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]

    # Create an InteractionsInterface instance
    interface = InteractionsInterface(interaction_matrix, type_colors, (100, 100), 500)

    # Simulate a mouse scroll up event at position (150, 150)
    mouse_pos = (150, 150)
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': mouse_pos, 'button': 4})  # Scroll up event

    # Apply the click event to modify interaction value
    interface.handle_click(event)

    # Check if the interaction value increased by 0.2 (expected value: 0.7)
    assert abs(interaction_matrix.interactions[(0, 1)] - 0.7) < 1e-6, \
        f"Expected 0.7 but got {interaction_matrix.interactions[(0, 1)]}"

# Pytest fixture to initialize and clean up pygame
@pytest.fixture(scope="module", autouse=True)
def init_pygame():
    pygame.init()
    yield
    pygame.quit()

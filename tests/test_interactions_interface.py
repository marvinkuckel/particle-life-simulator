import pygame
import pytest
from src.interactions import InteractionMatrix
from src.interactions_interface import InteractionsInterface

def test_handle_click():
    # Create a dummy interaction matrix
    interaction_matrix = InteractionMatrix(num_types=4, max_radius=0.5, min_radius=0, global_repulsion=0)
    interaction_matrix.interactions[(0, 1)] = 0.5

    # Create some dummy type colors
    type_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]

    # Create the InteractionsInterface instance
    interface = InteractionsInterface(interaction_matrix, type_colors, (100, 100), 500)

    # Simulate a click on the field (using a Pygame event)
    mouse_pos = (150, 150)  # Position inside the first field
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': mouse_pos, 'button': 4})  # Scroll up event

    # Handle the click
    interface.handle_click(event)

    # Use a tolerance to check if the interaction value has increased as expected
    assert abs(interaction_matrix.interactions[(0, 1)] - 0.7) < 1e-6, \
        f"Expected 0.7 but got {interaction_matrix.interactions[(0, 1)]}"


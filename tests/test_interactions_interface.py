# test_interactions_interface.py
import pytest
import pygame
from src.interactions import InteractionMatrix
from src.interactions_interface import InteractionsInterface

# Initialize Pygame (required to use Pygame's drawing functions)
pygame.init()

# Test for initializing the InteractionsInterface class
def test_interactions_interface_initialization():
    # Create a dummy interaction matrix
    interaction_matrix = InteractionMatrix(num_types=4, max_radius=0.5, min_radius=0, global_repulsion=0)
    interaction_matrix.interactions[(0, 1)] = 0.5
    interaction_matrix.interactions[(1, 2)] = -0.2

    # Create some dummy type colors
    type_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
    
    # Create the InteractionsInterface instance
    interface = InteractionsInterface(interaction_matrix, type_colors, (100, 100), 500)
    
    # Check that the instance is created successfully and has the correct attributes
    assert isinstance(interface, InteractionsInterface)
    assert interface.interaction_matrix == interaction_matrix
    assert interface.type_colors == type_colors
    assert interface.relative_position == (100, 100)
    assert interface.field_size > 0

# Test for drawing the interface (this would check if the drawing logic works without errors)
def test_draw_interactions_interface():
    # Create a dummy interaction matrix
    interaction_matrix = InteractionMatrix(num_types=4, max_radius=0.5, min_radius=0, global_repulsion=0)
    interaction_matrix.interactions[(0, 1)] = 0.5
    interaction_matrix.interactions[(1, 2)] = -0.2

    # Create some dummy type colors
    type_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]

    # Create the InteractionsInterface instance
    interface = InteractionsInterface(interaction_matrix, type_colors, (100, 100), 500)
    
    # Create a Pygame surface (simulate the drawing)
    surface = pygame.Surface((800, 600))
    
    # Draw the interface
    interface.draw(surface)

    # Assert that the drawing was done correctly (this will only ensure that no errors occur)
    # For more detailed tests, we could compare pixels or check the surface contents.
    assert surface is not None

# Test for handle_click method (ensuring clicking changes the interaction value)
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

    # Check if the interaction value has changed
    assert interaction_matrix.interactions[(0, 1)] == 0.7

# Run the tests
if __name__ == "__main__":
    pytest.main()

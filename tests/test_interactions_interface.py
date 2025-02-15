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
def handle_click(self, event: pygame.event.Event, adjust_by: float = 0.2):
    """Handles a mouse button event to modify interaction matrix values."""
    print(f"Received event: {event}")  # Debugging: Prüfen, ob das Event korrekt ankommt
    if result := pygame.Rect(event.pos, (1, 1)).collidedict(self.fields, values=True):
        key = result[0]
        interaction_value = self.interaction_matrix.interactions[key]
        print(f"Clicked on field: {key}, current value: {interaction_value}")  # Debugging: Prüfen, ob das richtige Feld erkannt wird
        
        if event.button == 4 and interaction_value < 1:
            new_value = round(interaction_value + adjust_by, 2)
            print(f"Updating interaction value from {interaction_value} to {new_value}")  # Debugging: Prüfen, ob der Wert aktualisiert wird
            self.interaction_matrix.interactions[key] = new_value
        elif event.button == 5 and interaction_value > -1:
            new_value = round(interaction_value - adjust_by, 2)
            print(f"Updating interaction value from {interaction_value} to {new_value}")
            self.interaction_matrix.interactions[key] = new_value

# Pygame setup and teardown for testing
@pytest.fixture(scope="module", autouse=True)
def init_pygame():
    pygame.init()
    yield
    pygame.quit()

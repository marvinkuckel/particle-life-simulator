
import unittest
from unittest.mock import MagicMock
import pygame
from typing import List, Tuple
from src.interactions_interface import InteractionsInterface

class TestInteractionsInterface(unittest.TestCase):
    def setUp(self):
        pygame.init()

        num_types = 3
        self.interaction_matrix = MagicMock()
        self.interaction_matrix.number_of_types = num_types
        self.interaction_matrix.interactions = {
            (0, 0): 0.5,
            (0, 1): -0.5,
            (0, 2): 0.2,
            (1, 0): -0.5,
            (1, 1): 0.0,
            (1, 2): 0.1,
            (2, 0): 0.2,
            (2, 1): 0.1,
            (2, 2): -0.2
        }
        
        self.type_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        self.top_left = (100, 100)
        self.right = 400

        self.interface = InteractionsInterface(self.interaction_matrix, self.type_colors, self.top_left, self.right)
        self.surface = MagicMock(spec=pygame.Surface)

    def test_draw(self):
        mouse_pos = (150, 150)
        with unittest.mock.patch("pygame.draw.rect") as mock_draw_rect:
            self.interface.draw(self.surface, mouse_pos)
            mock_draw_rect.assert_any_call(self.surface, (0, 255*0.5, 0), unittest.mock.ANY)
            mock_draw_rect.assert_any_call(self.surface, (255*0.5, 0, 0), unittest.mock.ANY)

    def test_handle_click(self):
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (150, 150), 'button': 4})
        initial_value = self.interaction_matrix.interactions[(0, 0)]
        self.interface.handle_click(event)
        self.assertEqual(self.interaction_matrix.interactions[(0, 0)], initial_value + 0.2)

    def test_handle_click_scroll_down(self):
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (150, 150), 'button': 5})
        initial_value = self.interaction_matrix.interactions[(0, 0)]
        self.interface.handle_click(event)
        self.assertEqual(self.interaction_matrix.interactions[(0, 0)], initial_value - 0.2)

    def test_handle_click_with_limit(self):
        self.interaction_matrix.interactions[(0, 0)] = -1
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (150, 150), 'button': 5})
        self.interface.handle_click(event)
        self.assertEqual(self.interaction_matrix.interactions[(0, 0)], -1)

    def tearDown(self):
        pygame.quit()

if __name__ == '__main__':
    unittest.main()
```
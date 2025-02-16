import unittest
import pygame
import sys
sys.path.insert(0, 'src')
from src.interactions_interface import InteractionsInterface
from src.interactions import InteractionMatrix

class TestInteractionsInterface(unittest.TestCase):

    def setUp(self):
        # initializes pygame and set up the display
        pygame.init()
        self.interaction_matrix = InteractionMatrix(num_types=4, max_radius=0.5, min_radius=0, global_repulsion=0)
        # set initial interaction value for (0, 1) to test the incrementation
        self.interaction_matrix.interactions[(0, 1)] = 0.5
        self.type_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
        self.interface = InteractionsInterface(self.interaction_matrix, self.type_colors, (100, 100), 500)
        self.screen = pygame.display.set_mode((800, 600))

    def test_handle_click(self):
        # simulate scrolling up and modify the interaction value
        mouse_pos = (270, 190)
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': mouse_pos, 'button': 4})  # Scroll up event
        self.interface.handle_click(event)

        # check if the interaction value increased by 0.2 as expected
        expected_value = 0.7
        actual_value = self.interaction_matrix.interactions[(0, 1)]
        self.assertAlmostEqual(actual_value, expected_value, delta=1e-6)

    def test_draw(self):
        # test draw method by confirming no exceptions occur
        try:
            self.interface.draw(self.screen, pygame.mouse.get_pos())
        except Exception as e:
            self.fail(f"Draw method raised an exception {e}")

    def tearDown(self):
        # clean up & quit
        pygame.quit()

if __name__ == "__main__":
    unittest.main()

import unittest
import numpy as np
from datetime import datetime
from unittest.mock import patch
import pygame
from simulation import aktualisiere_objekte, initialisiere_parameter, speichere_bild

class TestSimulation(unittest.TestCase):
    
    def test_aktualisiere_objekte(self):
        # Test the object update function
        positionen = np.random.rand(5, 2) * [1500, 1000]
        geschwindigkeiten = np.zeros((5, 2))
        kategorien = np.random.randint(0, 4, 5)
        min_abstand = np.random.uniform(30, 50, (4, 4))
        radius = np.random.uniform(70, 250, (4, 4))
        kraefte = np.random.uniform(0, 3, (4, 4))
        
        neue_positionen, neue_geschwindigkeiten = aktualisiere_objekte(positionen, geschwindigkeiten, kategorien, min_abstand, radius, kraefte)
        
        self.assertEqual(neue_positionen.shape, positionen.shape)
        self.assertEqual(neue_geschwindigkeiten.shape, geschwindigkeiten.shape)
    
    def test_initialisiere_parameter(self):
        # Test the parameter initialization function
        kraefte, min_abstand, radius = initialisiere_parameter()
        self.assertEqual(kraefte.shape, (4, 4))
        self.assertEqual(min_abstand.shape, (4, 4))
        self.assertEqual(radius.shape, (4, 4))
    
    @patch('pygame.image.save')  # Mocking pygame image save to avoid actual file saving
    def test_speichere_bild(self, mock_save):
        # Test the function to save images
        pygame.init()
        schirm = pygame.Surface((1500, 1000))  # Create a mock surface
        speichere_bild(schirm)
        # Check that the save method was called once
        self.assertTrue(mock_save.called)
    
if __name__ == '__main__':
    unittest.main()

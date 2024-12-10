import pygame
from .simulation import Simulation
from .gui import GUI

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    simulation = Simulation(screen, 800, 600)
    gui = GUI(screen, simulation)

    pygame.quit()

if __name__ == '__main__':
    main()

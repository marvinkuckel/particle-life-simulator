import sys

import pygame


from gui import GUI
from interactions import InteractionMatrix
from simulation import Simulation
class Main:
    
    def __init__(self, n_particles: int = 1000, n_types: int = 4):
        pygame.init()
        self.clock = pygame.time.Clock()
        
        # adjusts the window size to fit the current screen resolution
        self.width = pygame.display.Info().current_w
        self.height = pygame.display.Info().current_h
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.SCALED)

        self.interaction_matrix = InteractionMatrix(n_types, min_radius=0.01, max_radius=0.15, global_repulsion=0.015)
        self.simulation = Simulation(self.width, self.height, self.interaction_matrix, n_particles)
        
        simulation_controlls = {
            'start': self.simulation.start_simulation,
            'stop': self.simulation.stop_simulation,
            'reset': self.simulation.reset_simulation,
            'exit': lambda: pygame.event.post(pygame.event.Event(pygame.QUIT)),
        }
        
        self.gui = GUI(self.screen, self.width, self.height, self.interaction_matrix, simulation_controlls)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.gui.button_click(event)
                self.gui.draw_control_panel()

    def run(self, fps: int):
        self.running = True
        
        self.gui.draw_control_panel()
        while self.running:
            self.handle_events()
            dt = self.clock.tick(fps) / 1000  # time passed since last call in ms
            
            if not self.simulation.paused:
                self.simulation.update(dt)
                self.gui.draw_particles(self.simulation.particles)

            pygame.display.flip()

if __name__ == "__main__":
    app = Main(n_particles=1000)
    app.run(fps=30)
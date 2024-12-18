import sys
from typing import Tuple
import pygame
from colour import Color
from gui import GUI
from simulation import Simulation

class Main:
    def __init__(self, screen_size: Tuple[int, int], num_particles: int, num_types: int):
        self.width, self.height = screen_size
        
        pygame.init()
        self.screen = pygame.display.set_mode(screen_size)
        self.clock = pygame.time.Clock()

        self.simulation = Simulation(self.width, self.height, num_particles, num_types)
        self.simulation.setup_simulation()
        self.gui = GUI(self.screen, self.width, self.height, control_panel_width = self.width-self.height)
        
        colors = [Color(pick_for=t).rgb for t in range(num_types)]
        self.colors = [[x*255 for x in color] for color in colors]
        
    def run(self):
        self.running = True
        
        while self.running:
            # handle events/triggers
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                self.gui.handle_triggers(event)
                
            # update particles
            dt = self.clock.tick(60)  # 60 frames/sec
            self.simulation.update(dt)
            
            # draw new frame
            self.screen.fill(0)
            self.gui.draw_control_panel()
            self.simulation.render_frame(self.screen, self.colors)
            
            # update window
            pygame.display.flip()
        
if __name__ == "__main__":
    app = Main(screen_size=(1200, 800), num_particles=1000, num_types=5)
    app.run()

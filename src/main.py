<<<<<<< HEAD
import sys
from typing import Tuple
import pygame
from colour import Color
from gui import GUI
from simulation import Simulation

=======
import pygame
from typing import Tuple
<<<<<<< HEAD:main.py
from Simulation import Simulation
>>>>>>> 70ebcb30f2af92eee9137329a0f3e7122487b3b5
=======
from simulation import Simulation
>>>>>>> 96722d1c6ef946d028869d8a87838c22a42918cc:src/main.py

class Main:
    def __init__(self, screen_size: Tuple[int, int] = None):
        pygame.init()
        
        if screen_size is None:
            screen_size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        
        self.width, self.height = screen_size

        self.screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        
        self.simulation = Simulation(self.width, self.height)
        self.running = True
        self.started = False
        self.control_panel_width = self.width * 0.333

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.button_click(event)

    def button_click(self, event):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        start_button_x = self.width - self.control_panel_width + 20
        start_button_y = 50
        button_width = self.control_panel_width - 40
        button_height = 50
        stop_button_y = 110
        reset_button_y = 170

        # Start-Button
        if start_button_x < mouse_x < start_button_x + button_width and start_button_y < mouse_y < start_button_y + button_height:
            if not self.started:
                self.simulation.start_simulation()
                self.started = True

        # Stop-Button
        elif start_button_x < mouse_x < start_button_x + button_width and stop_button_y < mouse_y < stop_button_y + button_height:
            if self.started:
                self.simulation.stop_simulation()
                self.started = False
        
        # Reset-Button
        elif start_button_x < mouse_x < start_button_x + button_width and reset_button_y < mouse_y < reset_button_y + button_height:
            self.simulation.reset_simulation()
            self.started = False

        # Exit-Button
        elif start_button_x < mouse_x < start_button_x + button_width and reset_button_y + 60 < mouse_y < reset_button_y + 60 + button_height:
            self.running = False

    def run(self):
        while self.running:
            self.screen.fill((0, 0, 0))
            self.events()
            self.simulation.render_frame(self.screen)
            if self.started:
                self.simulation.update(0.1)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    app = Main()
    app.run()
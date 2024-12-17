import pygame
from typing import Tuple
from Simulation import Simulation


class Main:
    def __init__(self, screen_size: Tuple[int, int] = (1200, 800)):
        self.width, self.height = screen_size

        pygame.init()
        self.screen = pygame.display.set_mode(screen_size)
        self.clock = pygame.time.Clock()
        
        self.simulation = Simulation(self.width, self.height)
        self.running = True
        self.started = False

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.button_click()

    def button_click(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        button_x = self.width - self.width * 0.333 + 20
        button_y = 50
        button_width = self.width * 0.333 - 40
        button_height = 50
        if button_x < mouse_x < button_x + button_width and button_y < mouse_y < button_y + button_height:
            if not self.started:
                self.simulation.start_simulation()
                self.started = True

    def run(self):
        while self.running:
            self.screen.fill((0, 0, 0))
            self.events()
            self.simulation.render_frame(self.screen)
            if self.started:
                self.simulation.update(0.1)

            pygame.display.flip()
            self.clock.tick(60)  # 60 frames/sec

        pygame.quit()

if __name__ == "__main__":
    app = Main(screen_size=(1200, 800))
    app.run()
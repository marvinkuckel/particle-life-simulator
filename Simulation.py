import random
import pygame
from particle import Particle
from interactions import InteractionMatrix
from gui import GUI

class Simulation:
    def __init__(self, width, height, num_particles = 1000, num_types = 4, time_factor = 0.001):
        self.width = width
        self.height = height
        self.num_particles = num_particles
        self.num_types = num_types
        self.time_factor = time_factor
        self.particle_colors = {
            'christmas-red': (220, 20, 60),
            'christmas-green': (0, 128, 0),
            'christmas-white': (255, 255, 255),
            'christmas-gold': (255, 215, 0),
                                }
        self.type_colors = [color for color in self.particle_colors.values()]
        self.type_colors *= (self.num_types // len(self.type_colors)) + 1
        self.type_colors = self.type_colors[:self.num_types]

        self.particles = []

        self.gui = GUI(screen = None, screen_width = self.width, screen_height = self.height, control_panel_width = self.width * 0.333)

    def start_simulation(self):
        self.particles = [
            Particle(
                type = i % self.num_types,
                color = self.type_colors[i % len(self.type_colors)],
                size = 1,
                position = (random.random(), random.random()),
                velocity = (2 - random.random() * 4, 2 - random.random() * 4),
                friction = 0,
                random_movement = 0,
            )
            for i in range(self.num_particles)
        ]

    def render_frame(self, screen: pygame.display):
        control_panel_width = self.width * 0.333
        screen.fill((0, 0, 0))

        christmas_panel = pygame.Rect(self.width - control_panel_width, 0, control_panel_width, self.height)
        pygame.draw.rect(screen, (139, 24, 29), christmas_panel)

        pygame.draw.line(screen, (255, 255, 255), (self.width - control_panel_width, 0),
                         (self.width - control_panel_width, self.height), 2)

        for p in self.particles:
            p.draw(screen, self.width - control_panel_width, self.height, self.type_colors)

        self.gui.draw_buttons(screen, control_panel_width)

    def update(self, dt):
        for p in self.particles:
            p.update(dt, self.time_factor)
            if p.position[0] > (self.width - (self.width * 0.3)) / self.width:
                p.velocity[0] = -p.velocity[0]

    def enforce_boundaries(self):
        for p in self.particles:
            if p.position[0] < 0:
                p.position[0] = 0
                p.velocity[0] = -p.velocity[0]

            elif p.position[0] > 1:
                p.position[0] = 1
                p.velocity[0] = -p.velocity[0]

            if p.position[1] < 0:
                p.position[1] = 0
                p.velocity[1] = -p.velocity[1]

            elif p.position[1] > 1:
                p.position[1] = 1
                p.velocity[1] = -p.velocity[1]
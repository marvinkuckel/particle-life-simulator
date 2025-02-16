import sys

import cProfile
import pstats
import pygame
import time

from gui import GUI
from interactions import InteractionMatrix
from simulation import Simulation


# centralizes adjustment of all relevant parameters
simulation_parameters = {
    "n_particles": 2000,        # number of particles 
    "n_types": 4,               # number of particle types
    "time_factor": 0.1,         # controls simulation speed
    "force_scaling": 0.2,       # scales force acting on particles velocity
    "min_radius": 0.01,         # distance at which interaction starts and its force is strongest
    "max_radius": 0.15,         # distance at which interactions force is weakest and after which it stops
    "global_repulsion": 0.004,  # repulsive force acting on all particles
    "friction": 0.5,            # slows particles down over time
    "random_movement": 0        # adds random movement to particles position
}


class Main:
    
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        
        # adjusts the window size to fit the current screen resolution
        self.width = pygame.display.Info().current_w
        self.height = pygame.display.Info().current_h
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.SCALED)

        self.interaction_matrix = InteractionMatrix(
            simulation_parameters["n_types"],
            simulation_parameters["min_radius"],
            simulation_parameters["max_radius"],
            simulation_parameters["global_repulsion"]
        )

        self.simulation = Simulation(
            self.width, self.height,
            self.interaction_matrix,
            simulation_parameters["n_particles"],
            simulation_parameters["n_types"],
            simulation_parameters["time_factor"],
            simulation_parameters["force_scaling"],
            simulation_parameters["friction"],
            simulation_parameters["random_movement"]
        )

        simulation_controlls = {
            'start': self.simulation.start_simulation,
            'stop': self.simulation.stop_simulation,
            'reset': self.simulation.reset_simulation,
            'exit': lambda: pygame.event.post(pygame.event.Event(pygame.QUIT)),
            'set_sim_speed': self.simulation.adjust_time_factor,
            'get_sim_speed': self.simulation.get_time_factor,
            'set_force_scaling': self.simulation.set_force_scaling,
            'get_force_scaling': self.simulation.get_force_scaling,
            'set_particle_count': self.simulation.modify_particle_count,
            'get_particle_count': self.simulation.get_particle_count,
            'set_friction': self.simulation.set_friction,
            'get_friction': self.simulation.get_friction,
            'set_random_movement': self.simulation.set_random_movement,
            'get_random_movement': self.simulation.get_random_movement
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

    def run(self, fps: int):
        self.running = True
        
        while self.running:
            self.handle_events()
            dt = self.clock.tick(fps) / 1000  # time passed since last call in ms
            
            if not self.simulation.paused:
                self.simulation.update(dt)
                self.gui.draw_particles(self.simulation.particles)
            
            mouse_pos = pygame.mouse.get_pos()
            self.gui.draw_control_panel(mouse_pos)

            pygame.display.flip()

if __name__ == "__main__":
    app = Main()
    app.run(fps=30)
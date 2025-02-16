import sys
import cProfile
import pstats
import pygame
import time

from gui import GUI
from interactions import InteractionMatrix
from simulation import Simulation

# Centralizes adjustment of all relevant parameters
simulation_parameters = {
    "n_particles": 2000,        # Number of particles 
    "n_types": 5,               # Number of particle types
    "time_factor": 0.1,         # Controls simulation speed
    "force_scaling": 0.2,       # Scales force acting on particles velocity
    "min_radius": 0.01,         # Distance at which interaction starts and its force is strongest
    "max_radius": 0.15,         # Distance at which interactions force is weakest and after which it stops
    "global_repulsion": 0.004,  # Repulsive force acting on all particles
    "friction": 0.5,            # Slows particles down over time
    "random_movement": 0        # Adds random movement to particles position
}


class Main:
    
    def __init__(self):

        pygame.init()
        
        # Set up the clock to control the frame rate of the simulation
        self.clock = pygame.time.Clock()
        
        # Adjusts the window size to fit the current screen resolution
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
            'get_random_movement': self.simulation.get_random_movement,
            'particle_count': lambda: len(self.simulation.particles),
            'add_particles': self.simulation.add_particles,
            'remove_particles': self.simulation.remove_particles
        }
        
        # Create the GUI, passing in the necessary details such as screen dimensions, the interaction matrix, and the simulation controls
        self.gui = GUI(self.screen, self.width, self.height, self.interaction_matrix, simulation_controlls)

    def handle_events(self):
    # Loop through all the events in the pygame event queue
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If the user closes the window ...
            self.running = False  # ... set running to False to stop the game loop and ...
            pygame.quit()  # ... quit pygame and ...
            sys.exit()  # ... exit the program

        elif event.type == pygame.MOUSEBUTTONDOWN:  # If a mouse button is pressed ...
            self.gui.button_click(event)  # ... handle button click event in the GUI

    def run(self, fps: int):  # Define the main game loop
        """
        Runs the main game loop, continuously updating and rendering the simulation.
        The game loop handles all user input and events, updates the simulation if it's not paused, 
        and renders the simulation's particles and GUI elements on the screen. 
        It also refreshes the display to show the latest frame.
        """
        self.running = True
        
        while self.running:  # While the game is running
            self.handle_events()  # Handle user input
            dt = self.clock.tick(fps) / 1000  # Time passed since last call in ms
            
            if not self.simulation.paused:  # If the simulation is not paused ...
                self.simulation.update(dt)  # ... update the simulation and ...
                self.gui.draw_particles(self.simulation.particles)  # ... draw the particles
            
            mouse_pos = pygame.mouse.get_pos()  # Get the current mouse position
            self.gui.draw_control_panel(mouse_pos)  # Draw the control panel with the current mouse position

            pygame.display.flip()  # Updates the entire screen to show the latest drawing changes (Refresh)

if __name__ == "__main__":  # Ensures the script runs directly, not imported
    app = Main()  # Initializes the Main app
    app.run(fps=30)  # Runs the app with 30 FPS

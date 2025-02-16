import sys
import cProfile
import pstats
import pygame
import time

from gui import GUI
from interactions import InteractionMatrix
from simulation import Simulation

class Main:
    
    def __init__(self, n_particles: int = 1000, n_types: int = 4):
    
        # Initialise the Pygame library for graphical operations
        pygame.init()
        
        # Set up the clock to control the frame rate of the simulation
        self.clock = pygame.time.Clock()
        
        # Adjust the window size to match the current screen resolution
        self.width = pygame.display.Info().current_w  # Get the current screen width
        self.height = pygame.display.Info().current_h  # Get the current screen height
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.SCALED)  # Set the screen mode to the current resolution with scaling
        
        # Initialise the InteractionMatrix with specified parameters
        # The minimum and maximum radii and global repulsion define the interactions between particles
        self.interaction_matrix = InteractionMatrix(n_types, min_radius=0.01, max_radius=0.15, global_repulsion=0.006)
        
        # Create an instance of the Simulation class, passing in the screen dimensions and interaction matrix
        self.simulation = Simulation(self.width, self.height, self.interaction_matrix, n_particles)
        
        simulation_controlls = {
            'start': self.simulation.start_simulation,  # Start the simulation
            'stop': self.simulation.stop_simulation,    # Stop the simulation
            'reset': self.simulation.reset_simulation,  # Reset the simulation
            'exit': lambda: pygame.event.post(pygame.event.Event(pygame.QUIT)),  # Trigger the quit event to exit the application
        }
        
        # Create the GUI, passing in the necessary details such as screen dimensions, the interaction matrix, and the simulation controls
        self.gui = GUI(self.screen, self.width, self.height, self.interaction_matrix, simulation_controlls)

    def handle_events(self):
        """
        Handles the events within the Pygame event queue. 
        Specifically listens for quit events (e.g. closing the window) 
        and mouse button presses (for GUI interactions).

        1. Checks if the user has requested to quit the application.
        2. Processes mouse button clicks by triggering appropriate button actions.
        """
        mouse_pos = pygame.mouse.get_pos()  # Get the current mouse position
        
        for event in pygame.event.get():  # Iterate over the events in the event queue
            if event.type == pygame.QUIT:  # If the user has requested to quit ...
                self.running = False  # ... set the running flag to False and ...
                pygame.quit()  # ... quit the Pygame library and ...
                sys.exit()  # ... and exit the program

            elif event.type == pygame.MOUSEBUTTONDOWN:  # If the mouse button is pressed ...
                self.gui.button_click(event)  # ... check if the mouse is over a button and trigger the corresponding action ...
                self.gui.draw_control_panel(mouse_pos)  # ... and draw the control panel with the current mouse position

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

if __name__ == "__main__":  # If the script is run as the main module
    app = Main(n_particles=1000)  # Create an instance of the Main class
    app.run(fps=30)  # Run the main game loop with a frame rate of 30

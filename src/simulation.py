from interactions import InteractionMatrix, calculate_force
from particle import Particle
import numpy as np
import random

class Simulation:
    """
    Handles the particle simulation, including particle generation, interaction logic and grid management.
    """
    def __init__(self, width,
                 height,
                 interaction_matrix: InteractionMatrix,

                 num_particles=1000,  # <== Choose the amount of particles!
                 num_types=4,         # <== Choose the amount of particle types!
                 time_factor=0.1,     # <== Choose the speed of the simulation!
                 grid_size=10):       # <== Choose the size of the grid!
        
        self.width, self.height = width, height
        # Dynamically partitions simulation area into grid adjusted for screens aspect ratio
        # Cells count & size scales with particle number (more particles = more & smaller cells)
        self.grid_size = int((num_particles ** 0.5) * (width / height) ** 0.5)
        self.cells = {(x, y): np.empty(0, dtype=object) for x in range(self.grid_size) for y in range(self.grid_size)}

        self.num_particles = num_particles
        self.num_types = num_types
        self.time_factor = time_factor
        
        self.interaction_matrix = interaction_matrix
        self.particles = self.generate_particles()  # initialize particles

        self.paused = True

    def generate_particles(self):
        """
        Generates particles and adds them to the grid.
        """
        particles = np.empty(0, dtype=object)  # initialize particle array

        for i in range(self.num_particles):
            # Generates the number of particles specified, with the parameters set here
            particle = Particle(position=(random.random(), random.random()),  # Random initial position
                                velocity=(1 - random.random() * 2, 1 - random.random() * 2),  # Random initial velocity
                                type=i % self.num_types,  # Random particle type
                                size=1, friction=0.5, random_movement=0.01)  # Default particle properties

            particles = np.concatenate((particles, np.array([particle])))
            # Place particle in grid cell corresponding to initial position
            self.add_to_grid(particle)

        return particles

    def add_to_grid(self, particle):
        """
        Calculates cell coordinates by scaling position by the grid size and wraps around due to mod if applicable.
        """
        grid_x = int(particle.position[0] * self.grid_size) % self.grid_size
        grid_y = int(particle.position[1] * self.grid_size) % self.grid_size

        # Reashure that its always a numpy array (important for numba)
        if isinstance(self.cells[(grid_x, grid_y)], list):  # If it's a list ...
            self.cells[(grid_x, grid_y)] = np.array(self.cells[(grid_x, grid_y)], dtype=object)  # ... convert it to a numpy array

        if not isinstance(self.cells[(grid_x, grid_y)], np.ndarray):  # If it's not a numpy array ...
            self.cells[(grid_x, grid_y)] = np.empty(0, dtype=object)  # ... initialize it
        
        # Adds particle to appropriate cell 
        if self.cells[(grid_x, grid_y)].size == 0:  # If the cell is empty ...
            self.cells[(grid_x, grid_y)] = np.array([particle], dtype=object)  # ... add the particle

        else:  # If the cell is not empty ...
            self.cells[(grid_x, grid_y)] = np.concatenate((self.cells[(grid_x, grid_y)], np.array([particle])))  # ... add the particle

    def update(self, dt):
        """
        Clears grid for updating particle positions in one step.
        Updates particle position and adds it to appropriate cell
        """
        self.cells = {key: [] for key in self.cells}

        for p in self.particles:  # Iterate over the particles
            p.update_position(dt, self.time_factor)  # Update particle position
            self.add_to_grid(p)  # Add particle to appropriate cell

        # Iterates through all cells in the grid to calculate particle interactions
        for (grid_x, grid_y), particles in self.cells.items():
            for p1 in particles:
                # Checks interactions within the current cell and its neighboring cells
                for dx in (-1, 0, 1):  # Iterates over neighboring cells in the x-direction (left, center, right)
                    for dy in (-1, 0, 1):  # Iterates over neighboring cells in the y-direction (top, center, bottom)
                        neighbor_cell = (grid_x + dx, grid_y + dy)  # Identifies the neighboring cell
                        
                        # Checks if the neighboring cell exists in the grid
                        if neighbor_cell in self.cells:
                            for p2 in self.cells[neighbor_cell]:
                                # Avoids self-interaction (a particle with itself)
                                if p1 is not p2:
                                    # Calculates the interaction force between the two particles
                                    force_x, force_y = calculate_force(
                                        p1.position[0], p1.position[1], p1.type,
                                        p2.position[0], p2.position[1], p2.type,
                                        self.interaction_matrix.interactions,
                                        self.interaction_matrix.global_repulsion,
                                        self.interaction_matrix.max_radius,
                                        self.interaction_matrix.min_radius
                                    )
                                    # Applies the calculated force to particle p1
                                    p1.apply_force(force_x, force_y)

        self.enforce_boundaries()

    def enforce_boundaries(self):
        """
        Ensures that particles stay within the defined boundaries of the simulation area (between 0 and 1).
        If a particle goes out of bounds on either the x or y axis, its position and velocity are adjusted.
        """
        for p in self.particles:
            # Check if the particle is outside the boundaries along the x-axis
            if p.position[0] <= 0 or p.position[0] >= 1:  # If the particle is out of bounds over the x-axis ...
                p.position[0] = round(p.position[0])  # ... round its position and ...
                p.velocity[0] = -p.velocity[0]  # ... invert the particle's velocity

            if p.position[1] <= 0 or p.position[1] >= 1:  # If the particle is out of bounds over the y-axis ...
                p.position[1] = round(p.position[1])  # ... round its position and ...
                p.velocity[1] = -p.velocity[1]  # ... invert the particle's velocity

    def start_simulation(self):
        """
        Enerates particles if there are currently none.
        """
        self.paused = False
        if len(self.particles) == 0:  # If there are no particles ...
            self.particles = self.generate_particles()  # ... generate particles

    def stop_simulation(self):
        """
        Pauses the simulation.
        """
        self.paused = True              

    def reset_simulation(self):
        """
        Resets the simulation by removing all particles.
        """
        self.particles = np.array([], dtype=object)  # Empty particle array

import random
import time
import numpy as np

from particle import Particle
from interactions import InteractionMatrix, calculate_force


class Simulation:

    def __init__(self, width, height, interaction_matrix: InteractionMatrix, num_particles: int, num_types: int, time_factor: float, force_scaling: float, friction: float, random_movement: float):
            self.width, self.height = width, height

            # dynamically partitions simulation area into grid adjusted for screens aspect ratio
            # cells count & size scales with particle number (more particles = more & smaller cells)
            self.grid_size = int((num_particles ** 0.5) * (width / height) ** 0.5)
            self.cells = {(x, y): [] for x in range(self.grid_size) for y in range(self.grid_size)}
            
            self.interaction_matrix = interaction_matrix
            self.num_particles = num_particles
            self.num_types = num_types
            self.time_factor = time_factor

            # stores these values so particle can access the parameters set in main.py
            self.friction = friction  
            self.force_scaling = force_scaling 
            self.random_movement = random_movement

            self.particles = self.generate_particles()

            self.paused = True


    def generate_particles(self):
        particles = np.empty(0, dtype=object)

        # generates number of particles specified in main.py
        for i in range(self.num_particles):

            particle = Particle(
                position=(random.random(), random.random()),
                velocity=(1 - random.random() * 2, 1 - random.random() * 2),
                type=i % self.num_types,
                size=1,  
                friction=self.friction,
                force_scaling=self.force_scaling,
                random_movement=self.random_movement
            )

            particles = np.concatenate((particles, np.array([particle])))
            # place particle in grid cell corresponding to initial position
            self.add_to_grid(particle)

        return particles


    def add_to_grid(self, particle):
        # calculates cell coordinates by scaling position by the grid size and wraps around due to mod if applicable
        grid_x = int(particle.position[0] * self.grid_size) % self.grid_size
        grid_y = int(particle.position[1] * self.grid_size) % self.grid_size

        #reashure that its always a numpy array (important for numba)
        if isinstance(self.cells[(grid_x, grid_y)], list):
            self.cells[(grid_x, grid_y)] = np.array(self.cells[(grid_x, grid_y)], dtype=object)
        if not isinstance(self.cells[(grid_x, grid_y)], np.ndarray):
            self.cells[(grid_x, grid_y)] = np.empty(0, dtype=object)
        
        # adds particle to appropriate cell 
        if self.cells[(grid_x, grid_y)].size == 0:
            self.cells[(grid_x, grid_y)] = np.array([particle], dtype=object)
        else:
            self.cells[(grid_x, grid_y)] = np.concatenate((self.cells[(grid_x, grid_y)], np.array([particle])))


    def update(self, dt):

        # clears grid for updating particle positions in one step
        self.cells = {key: [] for key in self.cells}

        # updates particle position and adds it to appropriate cell
        for p in self.particles:
            p.update_position(dt, self.time_factor)
            self.add_to_grid(p)

        # calculates particle interactions within current and neighboring cells
        for (grid_x, grid_y), particles in self.cells.items():
            for p1 in particles:
                # checks current and surrounding cells
                for dx in (-1, 0, 1):       # checks self, left & right
                    for dy in (-1, 0, 1):   # checks self, top & bottom
                        neighbor_cell = (grid_x + dx, grid_y + dy)
                        # checks for existing, neighboring cells
                        if neighbor_cell in self.cells:
                            for p2 in self.cells[neighbor_cell]:
                                if p1 is not p2:    # no self interaction
                                    force_x, force_y = calculate_force(
                                        p1.position[0], p1.position[1], p1.type,
                                        p2.position[0], p2.position[1], p2.type,
                                        self.interaction_matrix.interactions,
                                        self.interaction_matrix.global_repulsion,
                                        self.interaction_matrix.max_radius,
                                        self.interaction_matrix.min_radius
                                    )
                                    p1.apply_force(force_x, force_y)

        self.enforce_boundaries()

    def enforce_boundaries(self):
        # enforces boundaries if particles are out of bounds on either axis
        for p in self.particles:
            if p.position[0] <= 0 or p.position[0] >= 1:
                # position is rounded to nearest axis
                p.position[0] = round(p.position[0])
                # velocity is inverted (particles bounce off of boundary)
                p.velocity[0] = -p.velocity[0]
                
            if p.position[1] <= 0 or p.position[1] >= 1:
                p.position[1] = round(p.position[1])
                p.velocity[1] = -p.velocity[1]
            

    def start_simulation(self):
        # generates particles if there are currently none
        self.paused = False
        if len(self.particles) == 0:    
            self.particles = self.generate_particles()


    def stop_simulation(self):
        self.paused = True              


    def reset_simulation(self):
        # removes all particles
        self.particles = np.array([], dtype=object)
    
    
    def add_particles(self, amount = 100):
        self.num_particles = amount
        
        new_particles = self.generate_particles()
        self.particles = np.concatenate((self.particles, new_particles))
        
        self.num_particles = len(self.particles)
    
    def remove_particles(self, amount = 100):
        self.particles = self.particles[:self.num_particles - amount]
        self.num_particles = len(self.particles) if len(self.particles) > 0 else 0
    
    
    def adjust_time_factor(self, by_percent: float):
        self.time_factor += self.time_factor * by_percent
        
    def get_time_factor(self):
        return self.time_factor
    
    
    def set_force_scaling(self, force_scaling: float):
        self.force_scaling = force_scaling
        
    def get_force_scaling(self):
        return self.force_scaling
        
        
    def modify_particle_count(self, by: int):
        if by > 0:
            self.num_types = by
            self.particles.extend(self.generate_particles())
            self.num_types = len(self.particles)
        else:
            self.particles = self.particles[:len(self.particles) - abs(by)]
            
    def get_particle_count(self):
        return len(self.particles)
            
    
    def set_friction(self, friction: float):
        """friction: number between 0 and 1"""
        for particle in self.particles:
            particle.friction = friction
            
    def get_friction(self):
        return self.particles[0].friction
    
    
    def set_random_movement(self, random_movement: float):
        """random_movement: should be close to 0 or be 0"""
        for particle in self.particles:
            particle.random_movement = random_movement

    def get_random_movement(self):
        return self.particles[0].random_movement

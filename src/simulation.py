import random
from particle import Particle
from interactions import InteractionMatrix


class Simulation:
    def __init__(self, width, height, interaction_matrix: InteractionMatrix, num_particles=1000, num_types=4, time_factor=0.1, grid_size=10):
        self.width, self.height = width, height
        # dynamically partitions simulation area into grid adjusted for screens aspect ratio
        # cells count & size scales with particle number (more particles = more & smaller cells)
        self.grid_size = int((num_particles ** 0.5) * (width / height) ** 0.5)
        self.cells = {(x, y): [] for x in range(self.grid_size) for y in range(self.grid_size)}

        self.num_particles = num_particles
        self.num_types = num_types
        self.time_factor = time_factor
        
        self.interaction_matrix = interaction_matrix
        self.particles = self.generate_particles()

        self.paused = True


    def generate_particles(self):
        particles = []

        for i in range(self.num_particles):
            # generates the number of particles specified, with the parameters set here
            particle = Particle(position=(random.random(), random.random()),
                                velocity=(1 - random.random() * 2, 1 - random.random() * 2),
                                type=i % self.num_types,
                                size=1, friction=0.5, random_movement=0.01)

            particles.append(particle)
            # place particle in grid cell corresponding to initial position
            self.add_to_grid(particle)

        return particles


    def add_to_grid(self, particle):
        # calculates cell coordinates by scaling position by the grid size and wraps around due to mod if applicable
        grid_x = int(particle.position[0] * self.grid_size) % self.grid_size
        grid_y = int(particle.position[1] * self.grid_size) % self.grid_size

        # adds particle to appropriate cell 
        self.cells[(grid_x, grid_y)].append(particle)


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
                                    force_x, force_y = self.interaction_matrix.calculate_force(p1, p2)
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
        self.particles = []              
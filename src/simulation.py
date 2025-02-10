import random
from particle import Particle
from interactions import InteractionMatrix

class Simulation:
    def __init__(self, width, height, interaction_matrix: InteractionMatrix, num_particles=1000, num_types=4, time_factor=0.1, grid_size=10):
        self.width, self.height = width, height
        # partitions the simulation area into cells 
        self.grid_size = grid_size
        self.cells = {(x, y): [] for x in range(grid_size) for y in range(grid_size)}
        
        self.num_particles = num_particles
        self.num_types = num_types
        self.time_factor = time_factor
        
        self.interaction_matrix = interaction_matrix
        self.particles = self.generate_particles()

        self.paused = True

    def generate_particles(self):
        particles = []

        for i in range(self.num_particles):
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
        # clears grid for updating particle movement
        for key in self.cells:
            self.cells[key] = []

        # updates particle position and adds it to appropriate cell
        for p in self.particles:
            p.update_position(dt, self.time_factor)
            self.add_to_grid(p)

        # checks each particle for interactions against others in its own and neighboring cells 
        for (grid_x, grid_y), particles in self.cells.items():
            for p1 in particles:
                # checks current and surrounding cells
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        neighbor_cell = (grid_x + dx, grid_y + dy)
                        # checks for neighboring cell
                        if neighbor_cell in self.cells:
                            for p2 in self.cells[neighbor_cell]:
                                # no self interaction
                                if p1 is not p2:
                                    force_x, force_y = self.interaction_matrix.calculate_force(p1, p2)
                                    p1.apply_force(force_x, force_y)
        
        self.enforce_boundaries()
        
    def enforce_boundaries(self):
        #Ensures particles do not get stuck at the borders by applying a soft repelling force.
        wall_bounce = 0.8        #force strength to prevent sticking
        for p in self.particles:
            if p.position[0] <= 0:     #if particle is at the left boundary
                p.position[0] = 0.01   #move it a lil bit away from the boundary
                p.velocity[0] = abs(p.velocity[0]) + wall_bounce  #reflect with a bit extra push
            elif p.position[0] >= 1:   #if particle is at the right boundary
                p.position[0] = 0.99   #move it a lil bit away from the boundary
                p.velocity[0] = -abs(p.velocity[0]) - wall_bounce  #reflect with a bit extra push
                
            if p.position[1] <= 0:     #if particle is at the top boundary
                p.position[1] = 0.01   #move it a little bit away from the boundary
                p.velocity[1] = abs(p.position[1]) + wall_bounce  #reflect with a bit extra push
            elif p.position[1] >= 1:   #if particle is at the bottom boundary
                p.position[1] = 0.99   #move it a little bit away from the boundary
                p.velocity[1] = -abs(p.position[1]) - wall_bounce #reflect with a bit extra push
            
    def start_simulation(self):
        self.paused = False
        if len(self.particles) == 0:  # no particles generated
            self.particles = self.generate_particles()

    def stop_simulation(self):
        self.paused = True

    def reset_simulation(self):
        self.particles = []
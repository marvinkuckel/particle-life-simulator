import random
from particle import Particle
from interactions import InteractionMatrix

class Simulation:
    def __init__(self, width, height, interaction_matrix: InteractionMatrix, num_particles = 1000, num_types = 4, time_factor = 0.1):
        self.width, self.height = width, height
        
        self.num_particles = num_particles
        self.num_types = num_types
        self.time_factor = time_factor
        
        self.interaction_matrix = interaction_matrix
        self.particles = self.generate_particles()

        self.paused = True

    def generate_particles(self):
        return [Particle(position = (random.random(), random.random()),
            velocity = (1 - random.random() * 2, 1 - random.random() * 2),
            type = i % self.num_types,
            size = 1, friction = 0.1, random_movement = 0)
          for i in range(self.num_particles)]

    def update(self, dt):
        for p1 in self.particles:
            for p2 in self.particles:
                if p1 is not p2:
                    force_x, force_y = self.interaction_matrix.calculate_force(p1, p2)
                    p1.apply_force(force_x, force_y)
        
        for p in self.particles:
            p.update_position(dt, self.time_factor)
        
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
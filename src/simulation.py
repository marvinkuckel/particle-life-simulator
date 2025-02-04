import random
from particle import Particle
from interactions import InteractionMatrix

class Simulation:
    def __init__(self, width, height, interaction_matrix: InteractionMatrix, num_particles=1000, num_types=4, time_factor=0.1):
        self.width, self.height = width, height
        self.num_particles = num_particles
        self.num_types = num_types
        self.time_factor = time_factor
        self.interaction_matrix = interaction_matrix
        self.particles = self.generate_particles()
        self.paused = True

    def generate_particles(self):
        particles = [
            Particle(position=(random.uniform(0, 1), random.uniform(0, 1)),
                     velocity=(random.uniform(-1, 1), random.uniform(-1, 1)),
                     type=i % self.num_types,
                     size=3, friction=0.1, random_movement=0)
            for i in range(self.num_particles)
        ]
        assert all(isinstance(p, Particle) for p in particles), "Fehler: Nicht alle Partikel sind korrekt initialisiert!"
        return particles

    def update(self, dt):
        if self.paused:
            return

        for p1 in self.particles:
            for p2 in self.particles:
                if p1 is not p2:
                    force_x, force_y = self.interaction_matrix.calculate_force(p1, p2)
                    p1.apply_force(force_x, force_y)

        for p in self.particles:
            p.update_position(dt, self.time_factor)

        self.enforce_boundaries()

    def enforce_boundaries(self):
        """Sorgt dafür, dass Partikel nicht aus dem Bildschirm verschwinden."""
        for p in self.particles:
            if p.position[0] <= 0 or p.position[0] >= 1:
                p.position[0] = max(0, min(p.position[0], 1))
                p.velocity[0] = -p.velocity[0]  # Reflexion

            if p.position[1] <= 0 or p.position[1] >= 1:
                p.position[1] = max(0, min(p.position[1], 1))
                p.velocity[1] = -p.velocity[1]

    def start_simulation(self):
        self.paused = False
        if len(self.particles) == 0:
            self.particles = self.generate_particles()

    def stop_simulation(self):
        self.paused = True

    def reset_simulation(self):
        self.particles = self.generate_particles()

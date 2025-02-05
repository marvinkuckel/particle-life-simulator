import sys
from typing import Tuple
import pygame
import numpy as np
from numba import jit
import os
from datetime import datetime

# Fensterparameter
class ParticleSimulation:
    def __init__(self, window_size: Tuple[int, int] = (1500, 1000), num_particles: int = 1000, num_types: int = 4):
        pygame.init()
        self.width, self.height = window_size
        self.screen = pygame.display.set_mode(window_size)
        pygame.display.set_caption("Particle Simulation")
        self.clock = pygame.time.Clock()
        self.num_particles = num_particles
        self.num_types = num_types
        self.color_step = 360 // num_types
        self.force_strength = 0.05
        self.friction = 0.85

        self.particles = [
            Particle(
                np.random.randint(0, num_types),
                2,
                np.random.rand(2) * [self.width, self.height]
            ) for _ in range(num_particles)
        ]
        self.type_ids = np.array([p.type_id for p in self.particles])
        self.forces, self.min_distance, self.radius = self.initialize_parameters()
        self.running = True
    
    def initialize_parameters(self):
        forces = np.random.uniform(0, 3, (self.num_types, self.num_types))
        forces[np.random.uniform(0, 1, (self.num_types, self.num_types)) < 0.5] *= -1
        min_distance = np.random.uniform(30, 50, (self.num_types, self.num_types))
        radius = np.random.uniform(70, 250, (self.num_types, self.num_types))
        return forces, min_distance, radius
    
    def save_screenshot(self):
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")
        filename = f"screenshots/particles_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        pygame.image.save(self.screen, filename)
    
    def update_particles(self):
        positions = np.array([p.position for p in self.particles])
        velocities = np.array([p.velocity for p in self.particles])
        positions, velocities = update_particles(positions, velocities, self.type_ids, self.min_distance, self.radius, self.forces)
        for i, p in enumerate(self.particles):
            p.position = positions[i]
            p.velocity = velocities[i]
            p.update_position()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.forces, self.min_distance, self.radius = self.initialize_parameters()
                elif event.key == pygame.K_s:
                    self.save_screenshot()
    
    def run(self, fps: int = 60):
        while self.running:
            self.handle_events()
            self.screen.fill((0, 0, 0))
            self.update_particles()
            for p in self.particles:
                p.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(fps)
        pygame.quit()

class Particle:
    def __init__(self, type_id: int, size, position, velocity=None, friction=0.85):
        self.type_id = type_id
        self.size = size
        self.position = np.array(position, dtype=np.float64)
        self.velocity = np.array(velocity if velocity is not None else [0, 0], dtype=np.float64)
        self.friction = friction
    
    def update_position(self):
        self.position += self.velocity
        self.velocity *= self.friction
        self.position[0] %= 1500  # Fensterbreite
        self.position[1] %= 1000  # Fensterhöhe
    
    def draw(self, screen):
        color = pygame.Color(0)
        color.hsva = (self.type_id * 90, 100, 100, 100)
        pygame.draw.circle(screen, color, (int(self.position[0]), int(self.position[1])), self.size)

@jit(nopython=True)
def update_particles(positions, velocities, type_ids, min_distance, radius, forces):
    num_particles = len(positions)
    new_positions = np.empty_like(positions)
    new_velocities = np.empty_like(velocities)
    for i in range(num_particles):
        total_force = np.array([0.0, 0.0])
        pos = positions[i]
        vel = velocities[i]
        type_i = type_ids[i]
        for j in range(num_particles):
            if i != j:
                direction = positions[j] - pos
                direction -= np.round(direction / np.array([1500, 1000])) * np.array([1500, 1000])
                distance = np.linalg.norm(direction)
                if distance > 0:
                    direction /= distance
                    type_j = type_ids[j]
                    if distance < min_distance[type_i, type_j]:
                        force_value = -3 * abs(forces[type_i, type_j]) * (1 - distance / min_distance[type_i, type_j])
                        total_force += direction * force_value
                    if distance < radius[type_i, type_j]:
                        force_value = forces[type_i, type_j] * (1 - distance / radius[type_i, type_j]) * 0.05
                        total_force += direction * force_value
        new_vel = vel * 0.85 + total_force
        new_pos = (pos + new_vel) % np.array([1500, 1000])
        new_positions[i] = new_pos
        new_velocities[i] = new_vel
    return new_positions, new_velocities

if __name__ == "__main__":
    sim = ParticleSimulation()
    sim.run()
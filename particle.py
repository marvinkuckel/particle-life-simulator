### particle.py 

import pygame # for creating a window, graphics, handling events etc.
import random # for random number generation

class Particle:
    def __init__(self, type, color, size, position, velocity, friction, random_movement):
        self.type = type
        self.color = color
        self.size = size
        self.position = position
        self.velocity = velocity
        self.friction = friction
        self.random_movement = random_movement

    def update(self):
        # updates position based on velocity
        self.position = (self.position[0] + self.velocity[0], self.position[1] + self.velocity[1])
        # updates position based on random movement
        self.position = (self.position[0] + random.uniform(-self.random_movement, self.random_movement),
                         self.position[1] + random.uniform(-self.random_movement, self.random_movement))
        # updates velocity based on friction
        self.velocity = (self.velocity[0] * self.friction, self.velocity[1] * self.friction)
        # implement bouncing back at edges
        pass
        
    def draw(self, screen):
        # draws particle on the screen created by pygame
        pygame.draw.circle(screen, self.color, (int(self.position[0]), int(self.position[1])), self.size)










### this part is used for testing

import sys # needed to exit the program

pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Create a particle
particle_1 = Particle('type1', (255, 0, 0), 5, (320, 240), (1, 1), 0.99, 2)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the particle
    particle_1.update()

    # Draw the particle
    screen.fill((0, 0, 0))  # Clear the screen with black
    particle_1.draw(screen)
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(60)

pygame.quit()
sys.exit()

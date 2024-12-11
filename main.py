import pygame
from Simulation import Simulation
from gui import GUI 

def main():
    pygame.init()
    #screen 
    screen_width, screen_height = 800, 600
    control_panel_width = 200
    screen = pygame.display.set_mode((screen_width + control_panel_width, screen_height))
    pygame.display.set_caption("Particle Life Simulator")

    #Simulation & GUI
    simulation = Simulation(screen_width, screen_height, screen)
    gui = GUI(screen, screen_width, screen_height, control_panel_width)

    running = True                #while simulation is running
    clock = pygame.time.Clock()   #clock for frame rate

    #main game loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            gui.handle_triggers(event)

        #Update & draw
        screen.fill((0, 0, 0))  
        simulation.update_simulation()
        simulation.render_frame()
        gui.control_panel()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
  

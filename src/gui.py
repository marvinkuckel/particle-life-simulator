from typing import Callable, Tuple
import pygame

from interactions_interface import InteractionsInterface

class Button():
    def __init__(self, pos: Tuple[int, int], size: Tuple[int, int], text: str, color: Tuple[int, int, int], action: Callable = None):
        """
        params:
            pos: (x, y) coordinates of buttons top-left corner
            size: (x, y) width and height of the button
            text: Text displayed on the button
            color: (r, g, b) Default color of the button
            action: execute event if button is clicked
        """
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.text = text
        self.color = color
        self.font = pygame.font.Font(None, 36)  # default font & size
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 3)

        # button text
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def trigger(self, event):
        # check if the button is clicked and trigger its action
        if event.type == pygame.MOUSEBUTTONDOWN:  # mouse-click?
            if self.rect.collidepoint(event.pos):  # mouse-click within button?
                if self.action:  # if there is an action, ...
                    self.action()  # trigger it.

class GUI:
    colors = {
            'simulation-background': (20, 20, 25),
            'panel-background': (25, 25, 35),
            'christmas-red': (220, 20, 60),
            'christmas-darkred': (150, 25, 30),
            'christmas-green': (0, 128, 0),
            'christmas-white': (255, 255, 255),
            'christmas-gold': (204, 153, 1),
            'christmas-grey': (40, 40, 50)
        }
    
    def __init__(self, screen, screen_width, screen_height, interaction_matrix, simulation_controlls: dict):
        self.screen = screen
        self.screen_width, self.screen_height = screen_width, screen_height
        self.control_panel_width = screen_width - screen_height
        
        self.particle_colors = [GUI.colors[key] for key in ['christmas-green','christmas-red','christmas-gold','christmas-white']]
        self.interaction_matrix = interaction_matrix
        
        self.buttons = []
        self.initiate_buttons(simulation_controlls)

        self.instruction_text = "Welcome to the Particle Life Simulator!"

        self.instruction_rect = pygame.Rect(self.screen_width - self.control_panel_width + 10, self.buttons[-1].rect.bottom + 180, self.control_panel_width - 20, 100)

        self.interactions_interface = InteractionsInterface(interaction_matrix, (screen_width-self.control_panel_width, self.buttons[-1].rect.bottom),
                                                            self.control_panel_width, 200, self.particle_colors)
        
    def draw_instruction(self):
        pygame.draw.rect(self.screen, self.colors['christmas-grey'], self.instruction_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), self.instruction_rect, 2)
        
        font = pygame.font.Font(None, 23)
        text_surface = font.render(self.instruction_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.instruction_rect.center)
        self.screen.blit(text_surface, text_rect)

    def initiate_buttons(self, simulation_controlls, h_padding = 60):
        # setup parameters for button initiation
        button_width = self.control_panel_width - 2*h_padding
        button_height = 50
        button_x = self.screen_width - self.control_panel_width + h_padding
        button_y = 50

        # Add buttons to the panel with the correct colors
        # self.buttons.append(Button((button_x, button_y), (button_width, button_height), "Start", (50, 86, 50), self.start_simulation))
        # self.buttons.append(Button((button_x, button_y + 60), (button_width, button_height), "Stop", (211, 171, 130), self.stop_simulation))
        # self.buttons.append(Button((button_x, button_y + 120), (button_width, button_height), "Reset", (123, 169, 191), self.reset))
        # self.buttons.append(Button((button_x, button_y + 180), (button_width, button_height), "Exit", (0, 0, 102), self.exit))
        self.buttons.append(Button((button_x, button_y), (button_width, button_height), "Start", self.colors['christmas-green'], simulation_controlls['start']))
        self.buttons.append(Button((button_x, button_y + 60), (button_width, button_height), "Stop", self.colors['christmas-gold'], simulation_controlls['stop']))
        self.buttons.append(Button((button_x, button_y + 120), (button_width, button_height), "Reset", self.colors['christmas-red'], simulation_controlls['reset']))
        self.buttons.append(Button((button_x, button_y + 180), (button_width, button_height), "Exit", self.colors['christmas-darkred'], simulation_controlls['exit']))

    def button_click(self, event):
        self.interactions_interface.handle_click(event)
        
        for button in self.buttons:
            if button.rect.collidepoint(event.pos):
                button.action()
                
    def draw_control_panel(self):
        pygame.draw.rect(self.screen, self.colors['panel-background'],
                         pygame.Rect(self.screen_width-self.control_panel_width, 0,
                                     self.control_panel_width, self.screen_height))
        
        for button in self.buttons:
            button.draw(self.screen)
            
        self.interactions_interface.draw(self.screen)

        self.draw_instruction()
 
    def draw_particles(self, particles):
        # reset canvas of simulation area
        pygame.draw.rect(self.screen, self.colors['simulation-background'], pygame.Rect(0, 0, self.screen_height + 1, self.screen_height + 1))
        
        for p in particles:
            color = self.particle_colors[p.type]
            p.draw(self.screen, self.screen_height, self.screen_height, color)
            
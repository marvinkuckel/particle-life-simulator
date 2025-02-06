from typing import Callable, Tuple
import pygame

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

class InteractionsInterface:
    class Field:
        def __init__(self, id: Tuple[int, int], relative_posititon: Tuple[int, int], size: int):
            self.id = id
            self.rect = pygame.Rect(relative_posititon, (size, size))
        
        def draw(self, surface: pygame.Surface, interaction_matrix: dict):
            interaction_value = interaction_matrix[self.id][0]
            color = (0, 255*interaction_value, 0) if interaction_value > 0 else (255*abs(interaction_value), 0, 0)
            pygame.draw.rect(surface, color, self.rect)
            
            
    def __init__(self, relative_position, panel_width, padding, interaction_matrix, type_colors):
        self.relative_position = relative_position[0]+30, relative_position[1]+10
        self.panel_size = panel_width
        self.padding = padding
        self.interaction_matrix = interaction_matrix
        self.type_colors = type_colors
        
        self.number_of_types = self.interaction_matrix.number_of_types
        self.field_size = (self.panel_size - 2*self.padding) / (self.number_of_types+1)
        
        self.initiate_fields()
        
    def initiate_fields(self):
        number_of_types, field_size = self.number_of_types, self.field_size
        
        self.fields = dict()
        for i in range(number_of_types):
            for j in range(number_of_types):
                # position = [self.relative_position[0] + (j+1)*field_size,
                #             self.relative_position[1] + (i+1)*field_size]
                # self.fields[(i, j)] = self.Field((i, j), relative_posititon = position, size = field_size)
                self.fields[(i, j)] = pygame.Rect(self.relative_position[0] + (i+1)*field_size,
                                                  self.relative_position[1] + (j+1)*field_size,
                                                  field_size, field_size)
                
    def draw(self, surface):
        self.__draw_type_indicators(surface)
        for field_index, field_rect in self.fields.items():
            interaction_value = self.interaction_matrix.interactions[field_index][0]
            color = (0, 255*interaction_value, 0) if interaction_value > 0 else (255*abs(interaction_value), 0, 0)
            pygame.draw.rect(surface, color, field_rect)
    
    def __draw_type_indicators(self, surface):
        size = self.field_size
        radius = self.field_size/2 - 30
        for i, color in enumerate(self.type_colors, start=1):
            pygame.draw.circle(surface, color, radius=radius, center=(self.relative_position[0] + i*size + size/2,
                                                                      self.relative_position[1] + size/2))
            pygame.draw.circle(surface, color, radius=radius, center=(self.relative_position[0] + size/2,
                                                                      self.relative_position[1] + i*size + size/2))
    
    def handle_click(self, event):
        if result := pygame.Rect(event.pos, (1,1)).collidedict(self.fields, values=True):
            key = result[0]
            interaction_value = self.interaction_matrix.interactions[key][0]
            if event.button == 4 and interaction_value < 1:
                self.interaction_matrix.interactions[key][0] = round(interaction_value + 0.1, 2)
            if event.button == 5 and interaction_value > -1:
                self.interaction_matrix.interactions[key][0] = round(interaction_value - 0.1, 2)
        

class GUI:
    colors = {
            'simulation-background': (20, 20, 25),
            'panel-background': (25, 25, 35),
            'christmas-red': (220, 20, 60),
            'christmas-darkred': (150, 25, 30),
            'christmas-green': (0, 128, 0),
            'christmas-white': (255, 255, 255),
            'christmas-gold': (204, 153, 1)
        }
    
    def __init__(self, screen, screen_width, screen_height, interaction_matrix, simulation_controlls: dict):
        self.screen = screen
        self.screen_width, self.screen_height = screen_width, screen_height
        self.control_panel_width = screen_width - screen_height
        
        self.particle_colors = [GUI.colors[key] for key in ['christmas-green','christmas-red','christmas-gold','christmas-white']]
        self.interaction_matrix = interaction_matrix
        
        self.buttons = []
        self.initiate_buttons(simulation_controlls)
        self.interactions_interface = InteractionsInterface((screen_width-self.control_panel_width, self.buttons[-1].rect.bottom),
                                                            self.control_panel_width, 150, interaction_matrix, self.particle_colors)

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
            
    def draw_particles(self, particles):
        # reset canvas of simulation area
        pygame.draw.rect(self.screen, self.colors['simulation-background'], pygame.Rect(0, 0, self.screen_height + 1, self.screen_height + 1))
        
        for p in particles:
            color = self.particle_colors[p.type]
            p.draw(self.screen, self.screen_height, self.screen_height, color)
            
from typing import Callable, Tuple
import pygame
import time

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
        self.font = pygame.font.Font(None, 36)
        self.action = action
        self.original_color = color
        self.hover_color = self.lighten_color(color, factor=2)
        self.clicked_color = self.darken_color(color, factor=0.7)
        self.is_clicked = False
        self.clicked_time = 0
        self.size_factor = 1

    def lighten_color(self, color, factor):
        return tuple(min(int(c * factor), 255) for c in color)
    
    def darken_color(self, color, factor):
        return tuple(max(int(c * factor), 0) for c in color)

    def draw(self, screen, mouse_pos):
        if self.is_clicked and time.time() - self.clicked_time > 0.3:
            self.is_clicked = False
            self.size_factor = 1

        if self.rect.collidepoint(mouse_pos):
            current_color = self.hover_color
        else:
            current_color = self.color

        width = int(self.rect.width * self.size_factor)
        height = int(self.rect.height * self.size_factor)
        rect = pygame.Rect(self.rect.x + (self.rect.width - width) // 2, 
                        self.rect.y + (self.rect.height - height) // 2, width, height)

        pygame.draw.rect(screen, current_color, rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, 3)

        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)

    def trigger(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:  # mouse-click?
            if self.rect.collidepoint(event.pos):  # mouse-click within button?
                if self.action:  # if there is an action, ...
                    self.action()  # trigger it.
                self.is_clicked = True
                self.clicked_time = time.time()
                self.size_factor = 0.95

class GUI:
    colors = {
            'simulation-background': (20, 20, 25),
            'panel-background': (25, 25, 35),
            'christmas-red': (220, 20, 60),
            'christmas-darkred': (150, 25, 30),
            'christmas-green': (0, 128, 0),
            'christmas-white': (255, 255, 255),
            'christmas-gold': (204, 153, 1),
            'christmas-grey': (80, 90, 120),
            'christmas-blue': (0, 30, 250)
        }
    
    def __init__(self, screen, screen_width, screen_height, interaction_matrix, simulation_controlls: dict):
        self.screen = screen
        self.screen_width, self.screen_height = screen_width, screen_height
        self.control_panel_width = screen_width - screen_height
        
        self.particle_colors = [self.colors[key] for key in ['christmas-green','christmas-red','christmas-gold','christmas-white']]
        self.interaction_matrix = interaction_matrix
        
        self.buttons = []
        self.initiate_buttons(simulation_controlls)

        self.interactions_interface = InteractionsInterface(interaction_matrix, (screen_width-self.control_panel_width, self.buttons[-1].rect.bottom),
                                                            self.control_panel_width, 200, self.particle_colors)

        if self.interactions_interface.fields:
            last_field_bottom = list(self.interactions_interface.fields.values())[-1].bottom
            self.instruction_rect = pygame.Rect(self.screen_width - self.control_panel_width + 10, 
                last_field_bottom + 20, self.control_panel_width - 20, 250)
        else:
            self.instruction_rect = pygame.Rect(self.screen_width - self.control_panel_width + 10, 
                                                180, self.control_panel_width - 20, 250)

    def draw_instruction(self):
        pygame.draw.rect(self.screen, self.colors['christmas-grey'], self.instruction_rect)
        pygame.draw.rect(self.screen, (250, 5, 80), self.instruction_rect, 3)

        font = pygame.font.Font(None, 23)
        header_font = pygame.font.Font(None, 28)
        header_font.set_bold(True)
        header_font.set_italic(True)
        
        y_offset = self.instruction_rect.top + 25

        header_parts = ["Welcome to the", "Particle", "Life", "Simulator", "!"]
        segment_colors = [
            self.colors['christmas-white'],
            self.colors['christmas-red'],
            self.colors['christmas-gold'],
            self.colors['christmas-green'],
            self.colors['christmas-white']
        ]

        x_offset = self.instruction_rect.centerx - sum(header_font.size(word)[0] for word in header_parts) / 2

        for idx, part in enumerate(header_parts):
            shadow_surface = header_font.render(part, True, (0, 0, 0))
            shadow_rect = shadow_surface.get_rect(topleft=(x_offset + 1, y_offset + 1))
            self.screen.blit(shadow_surface, shadow_rect)

            part_surface = header_font.render(part, True, segment_colors[idx])
            part_rect = part_surface.get_rect(topleft=(x_offset, y_offset))
            self.screen.blit(part_surface, part_rect)

            x_offset += part_surface.get_width()

        y_offset += header_font.get_height()

        color_words = {
            "Start": self.colors['christmas-green'],
            "Stop": self.colors['christmas-gold'],
            "Reset": self.colors['christmas-red'],
            "Exit": self.colors['christmas-blue']
        }

        instruction_parts = [
            "Click Start to activate the particles.",
            "While they are moving, you can press Stop to pause the simulation.",
            "To clear the screen and restart, use Reset button.",
            "Click Exit to leave the simulation.",
            "Thank you!"
        ]

        total_text_height = sum(font.get_height() + 10 for line in instruction_parts) + header_font.get_height()

        y_offset = self.instruction_rect.top + 80

        x_offset = self.instruction_rect.left - 20

        for line in instruction_parts:
            words = line.split(" ")
            centered_x_offset = x_offset + (self.instruction_rect.width - sum(font.size(word)[0] for word in words)) / 2

            for word in words:
                if word.strip("'") in color_words:
                    color = color_words[word.strip("'")]
                else:
                    color = self.colors['christmas-white']

                shadow_surface = font.render(word, True, (0, 0, 0))
                shadow_rect = shadow_surface.get_rect(topleft=(centered_x_offset + 1, y_offset + 1))
                self.screen.blit(shadow_surface, shadow_rect)

                word_surface = font.render(word, True, color)
                word_rect = word_surface.get_rect(topleft=(centered_x_offset, y_offset))
                self.screen.blit(word_surface, word_rect)

                centered_x_offset += word_surface.get_width() + font.size(" ")[0]

            y_offset += font.get_height() + 15

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
        self.buttons.append(Button((button_x, button_y + 180), (button_width, button_height), "Exit", self.colors['christmas-blue'], simulation_controlls['exit']))

    def button_click(self, event):
        self.interactions_interface.handle_click(event)
        
        for button in self.buttons:
            if button.rect.collidepoint(event.pos):
                button.trigger(event)
                
    def draw_control_panel(self, mouse_pos):
        pygame.draw.rect(self.screen, self.colors['panel-background'],
                         pygame.Rect(self.screen_width-self.control_panel_width, 0,
                                     self.control_panel_width, self.screen_height))
        
        for button in self.buttons:
            button.draw(self.screen, mouse_pos)
            
        self.interactions_interface.draw(self.screen)

        self.draw_instruction()
            
    def draw_particles(self, particles):
        # reset canvas of simulation area
        pygame.draw.rect(self.screen, self.colors['simulation-background'], pygame.Rect(0, 0, self.screen_height + 1, self.screen_height + 1))
        
        for p in particles:
            color = self.particle_colors[p.type]
            p.draw(self.screen, self.screen_height, self.screen_height, color)

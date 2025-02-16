import os
from typing import Tuple
import time

import pygame

from interactions_interface import InteractionsInterface

class Text:
    """Simple text that can be updated by a get function and drawn in draw_control_panel"""
    def __init__(self, text, font_size, center, font_color = (255, 255, 255), get_value: callable = None, length = None):
        self.text = text
        self.length = length
        self.get_value = get_value
        
        self.font = pygame.font.Font(None, font_size)
        self.font_color = font_color
        
        self.rendered_text = self.font.render(text, True, font_color)
        self.rect = self.rendered_text.get_rect(center=center)
    
    def draw(self, screen):
        screen.blit(self.rendered_text, self.rect)
        
    def set_text(self, text):
        self.rendered_text = self.font.render(text, True, self.font_color)
        #self.rect = self.rendered_text.get_rect(center=self.rect.center)
        
    def update(self):
        if self.get_value:
            text = str(round(self.get_value(), 4))
            
            # keep text the same length
            if self.length:
                while len(text) < self.length:
                    text = text + "0"
                if len(text) > self.length:
                    text = text[:self.length]
                
            self.set_text(text)


class Button():
    def __init__(self, pos: Tuple[int, int], size: Tuple[int, int], text: str, color: Tuple[int, int, int], action: callable = None, font_size = 36, image_name = None):
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
        self.font = pygame.font.Font(None, font_size)
        self.action = action
        self.original_color = color
        self.hover_color = self.lighten_color(color, factor=2)
        self.clicked_color = self.darken_color(color, factor=0.7)
        self.is_clicked = False
        self.clicked_time = 0
        self.size_factor = 1
        
        self.image = None
        if image_name:
            size = self.rect.size[0] - 10, self.rect.size[1] - 10
            
            cwd = os.getcwd()
            path1 = os.path.join(cwd, "images", image_name)
            path2 = os.path.join(cwd, "src", "images", image_name)
            
            try:
                self.image = pygame.image.load(path1)
                self.image = pygame.transform.scale(self.image, size)
            except:
                try:
                    self.image = pygame.image.load(path2)
                    self.image = pygame.transform.scale(self.image, size)
                except:
                    print("Image could not be loaded. Displaying text instead")
                    

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

        if self.image:
            pos = self.rect.topleft
            screen.blit(self.image, (pos[0] + 5, pos[1] + 5))
        else:
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


class Slider:
    def __init__(self, left_x, right_x, center_y, min_value, max_value, setter: callable, getter: callable):
        self.x, self.y = left_x, center_y
        self.min_value, self.max_value = min_value, max_value
        self.setter, self.getter = setter, getter
        
        self.width = right_x - left_x
        self.slider_pos = self.x + self.width * (getter() / max_value - min_value)
        self.rect = pygame.Rect(self.x - 7, self.y - 7, self.width + 14, 14)
        
    def update(self, x_position):
        self.slider_pos = min(max(x_position, self.x), self.x + self.width)
        value = (x_position - self.x) / self.width * (self.max_value - self.min_value)
        self.setter(max(min(value, self.max_value), self.min_value))

    def draw(self, surface):
        pygame.draw.line(surface, (80, 80, 80), (self.x, self.y), (self.x+self.width, self.y), 3)
        pygame.draw.circle(surface, (0, 0, 0), (self.slider_pos, self.y), 7)
        pygame.draw.circle(surface, (160, 160, 160), (self.slider_pos, self.y), 4)
    

class GUI:
    colors = {
            'simulation-background': (20, 20, 25),
            'panel-background': (25, 25, 35),
            'normal-button': (40, 40, 40),
            'christmas-red': (220, 20, 60),
            'christmas-darkred': (150, 25, 30),
            'christmas-green': (0, 128, 0),
            'christmas-white': (255, 255, 255),
            'christmas-gold': (204, 153, 1),
            'christmas-grey': (80, 90, 120),
            'christmas-blue': (0, 30, 250)
        }
    
    def __init__(self, screen, screen_width, screen_height, interaction_matrix, simulation_controlls: dict, padding: int = 60):
        self.screen = screen
        self.screen_width, self.screen_height = screen_width, screen_height
        self.control_panel_width = screen_width - screen_height
        self.padding = padding  # distance between panel elementens and panel boundaries/borders
        
        self.particle_colors = [self.colors[key] for key in ['christmas-green','christmas-red','christmas-gold','christmas-white','christmas-blue']]
        self.interaction_matrix = interaction_matrix
        
        self.text_fields = []
        self.sliders = []
        
        self.buttons = []
        self.initiate_main_buttons(simulation_controlls, h_padding = self.padding)
        
        self.interactions_interface = InteractionsInterface(interaction_matrix, self.particle_colors,
                                                            top_left = (screen_width - self.control_panel_width//2, self.buttons[-1].rect.bottom),
                                                            right = self.screen_width - self.padding)

        if self.interactions_interface.fields:
            last_field_bottom = list(self.interactions_interface.fields.values())[-1].bottom
            self.instruction_rect = pygame.Rect(self.screen_width - self.control_panel_width + 10, 
                last_field_bottom + 20, self.control_panel_width - 20, 250)
        else:
            self.instruction_rect = pygame.Rect(self.screen_width - self.control_panel_width + 10, 
                                                180, self.control_panel_width - 20, 250)
        
        self.initiate_secondary_buttons(simulation_controlls)

    def draw_instruction(self):
        pygame.draw.rect(self.screen, self.colors['christmas-grey'], self.instruction_rect)
        pygame.draw.rect(self.screen, (250, 5, 80), self.instruction_rect, 3)

        font = pygame.font.Font(None, 18)
        header_font = pygame.font.Font(None, 23)
        header_font.set_bold(True)
        header_font.set_italic(True)
        
        y_offset = self.instruction_rect.top + 10

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
            "Exit": self.colors['christmas-blue'],
            "attraction": (0, 224, 0),
            "repulsion": (224, 0, 0)
        }

        instruction_parts = [
            "Click Start to activate the particles.",
            "While they are moving, you can press Stop to pause the simulation.",
            "To clear the screen and restart, use Reset button.",
            "Click Exit to leave the simulation.",
            "Thank you!",
            "",
            "_____ Matrix Controls _____",
            "Increase attraction - left mouse button / scroll upwards",
            "Increase repulsion - right mouse button / scroll downwards"
        ]

        y_offset = self.instruction_rect.top + 30

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

            y_offset += font.get_height() + 5
            
        # set the height so the text fits inside
        self.instruction_rect.height = y_offset - self.instruction_rect.top + 10
        self.instruction_rect.bottom = self.screen_height - 10

    def initiate_main_buttons(self, simulation_controlls, h_padding = 60):
        # setup parameters for button initiation
        button_width = self.control_panel_width - 2*h_padding
        button_height = 50
        button_x = self.screen_width - self.control_panel_width + h_padding
        button_y = 50

        self.buttons.append(Button((button_x, button_y), (button_width, button_height), "Start", self.colors['christmas-green'], simulation_controlls['start']))
        self.buttons.append(Button((button_x, button_y + 60), (button_width, button_height), "Stop", self.colors['christmas-gold'], simulation_controlls['stop']))
        self.buttons.append(Button((button_x, button_y + 120), (button_width, button_height), "Reset", self.colors['christmas-red'], simulation_controlls['reset']))
        self.buttons.append(Button((button_x, button_y + 180), (button_width, button_height), "Exit", self.colors['christmas-blue'], simulation_controlls['exit']))

    def initiate_secondary_buttons(self, simulation_controls):
        """Buttons for managing parameters influencing the particle interactions
        Call this method after creating interactions_interface"""
        font = pygame.font.Font(None, 24)
        
        relative_x = self.screen_width - self.control_panel_width + self.padding//2
        relative_y = self.buttons[-1].rect.bottom + 50
        
        section_width = self.screen_width - self.control_panel_width//2 - relative_x - 10
        center_x = relative_x + section_width//2
        
        # ------ simulation speed ------
        font_size = font.size("0.000")
        options = [-0.25, -0.1, -0.02, 0.02, 0.1, 0.25]
        button_size = (section_width - font_size[0] - 25) // len(options)
        
        for i, change_by in enumerate(options):
            func = lambda change=change_by: simulation_controls['set_sim_speed'](change)
                
            sign = "+" if change_by > 0 else "-"
            text = sign + str(int(abs(change_by) * 100)) + "%"
            
            offset = 0 if i < len(options)//2 else font_size[0] + 20
            self.buttons.append(Button((relative_x + i*(button_size + 4) + offset, relative_y), (button_size, button_size),
                                       text, self.colors["normal-button"], func,
                                       font_size=button_size//2))

        setting_name = Text("Simulation Speed", 26, center=(center_x, self.buttons[-1].rect.top - 20))
        setting_value = Text("0.0000", 24, (center_x + 5, self.buttons[-1].rect.center[1]), get_value=simulation_controls['get_sim_speed'], length=6)
        self.text_fields.extend((setting_name, setting_value))
        
        relative_x += 8
        
        # ----- force scaling -----
        y = self.buttons[-1].rect.bottom + 20
        self.text_fields.append(Text("Force Scaling", 18, center=(relative_x + section_width//4 - 7, y)))
        self.sliders.append(Slider(relative_x, relative_x + section_width//2 - 20, self.text_fields[-1].rect.bottom + 10, 0.001, 1,
                                   simulation_controls['set_force_scaling'], simulation_controls['get_force_scaling']))
        
        # ----- friction -----
        self.text_fields.append(Text("Friction", 18, center=(relative_x + section_width*3//4 - 7, y)))
        self.sliders.append(Slider(relative_x + section_width//2, relative_x + section_width - 15, self.text_fields[-1].rect.bottom + 10, 0, 1,
                                   simulation_controls['set_friction'], simulation_controls['get_friction']))
        
        # ----- random movement ----
        y = self.sliders[-1].rect.bottom + 20
        self.text_fields.append(Text("Random Movement", 18, center=(relative_x + section_width//4 - 7, y)))
        self.sliders.append(Slider(relative_x, relative_x + section_width//2 - 20, self.text_fields[-1].rect.bottom + 10, 0, 0.05,
                                   simulation_controls['set_random_movement'], simulation_controls['get_random_movement']))
        
        # ----- global repulsion -----
        self.text_fields.append(Text("Global Repulsion", 18, center=(relative_x + section_width*3//4 - 7, y)))
        self.sliders.append(Slider(relative_x + section_width//2, relative_x + section_width - 20, self.text_fields[-1].rect.bottom + 10, 0.0001, 0.01,
                                   self.interaction_matrix.set_global_repulsion, self.interaction_matrix.get_global_repulsion))
        
        # ----- min radius -----
        y = self.sliders[-1].rect.bottom + 20
        self.text_fields.append(Text("Min Radius", 18, center=(relative_x + section_width//4 - 7, y)))
        self.sliders.append(Slider(relative_x, relative_x + section_width//2 - 20, self.text_fields[-1].rect.bottom + 10, 0.00001, 0.049,
                                   self.interaction_matrix.set_min_radius, self.interaction_matrix.get_min_radius))
        
        # ----- max radius -----
        self.text_fields.append(Text("Max Radius", 20, center=(relative_x + section_width*3//4 - 7, y)))
        self.sliders.append(Slider(relative_x + section_width//2, relative_x + section_width - 20, self.text_fields[-1].rect.bottom + 10, 0.05, 0.3,
                                   self.interaction_matrix.set_max_radius, self.interaction_matrix.get_max_radius))
        
        # ----- randomize matrix fields -----
        pos = self.interactions_interface.relative_position
        first_field_rect = self.interactions_interface.fields[0, 0]
        
        self.buttons.append(Button((0, 0), (30, 30), "", self.colors['normal-button'], self.interaction_matrix.randomize_fields, image_name="refresh.png"))
        self.buttons[-1].rect.bottomright = first_field_rect.topleft
        
        # ----- particle count -----
        self.text_fields.append(Text("Particles: ", 24, (0, self.sliders[-2].rect.bottom + 25)))
        self.text_fields[-1].rect.left = relative_x + 8
        self.text_fields.append(Text("1000", 20, (self.text_fields[-1].rect.right + 20, self.text_fields[-1].rect.centery), get_value=simulation_controls['particle_count']))
        
        self.buttons.append(Button((self.text_fields[-1].rect.right + 20, self.text_fields[-1].rect.top), (40, 25), "-100",
                                   self.colors['normal-button'], simulation_controls['remove_particles'], font_size = 16))
        self.buttons.append(Button((self.buttons[-1].rect.right + 10, self.buttons[-1].rect.top), (40, 25), "+100", 
                                   self.colors['normal-button'], simulation_controls['add_particles'], font_size = 16))
        
        center_y = self.text_fields[-1].rect.centery
        self.buttons[-1].rect.centery = center_y
        self.buttons[-2].rect.centery = center_y
        
    def button_click(self, event):
        for button in self.buttons:
            if button.rect.collidepoint(event.pos):
                button.trigger(event)
                if button.text.lower() == "reset":
                    self.draw_particles([])
                return
        
        for slider in self.sliders:
            if slider.rect.collidepoint(event.pos):
                print(event.pos, slider.rect, slider.rect.collidepoint(event.pos))
                slider.update(event.pos[0])
                return
        
        self.interactions_interface.handle_click(event)
                
    def draw_control_panel(self, mouse_pos):
        pygame.draw.rect(self.screen, self.colors['panel-background'],
                         pygame.Rect(self.screen_width-self.control_panel_width, 0,
                                     self.control_panel_width, self.screen_height))
        
        for text in self.text_fields:
            text.update()
            text.draw(self.screen)
        
        for button in self.buttons:
            button.draw(self.screen, mouse_pos)
            
        for slider in self.sliders:
            slider.draw(self.screen)
            
        self.interactions_interface.draw(self.screen, mouse_pos)

        self.draw_instruction()
            
    def draw_particles(self, particles):
        # reset canvas of simulation area
        pygame.draw.rect(self.screen, self.colors['simulation-background'], pygame.Rect(0, 0, self.screen_height + 1, self.screen_height + 1))
        
        for p in particles:
            color = self.particle_colors[p.type]
            p.draw(self.screen, self.screen_height, self.screen_height, color)

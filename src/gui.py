import pygame
from simulation import *

class Button():
    def __init__(self, x, y, width, height, text, color, action=None):
        """
        x: X-coordinate of the button
        y: Y-coordinate of the button
        width: Button width
        height: Button height
        text: Text displayed on the button
        color: Default color of the button
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.font = pygame.font.Font(None, 36)  # default font & size
        self.action = action

    def draw_button(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

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

class GUI():
    def __init__(self, screen, screen_width, screen_height, control_panel_width):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.control_panel_width = control_panel_width
        self.buttons = []
        self.buttons_for_panel()

    def buttons_for_panel(self):
        # Make buttons for the control panel
        button_width = self.control_panel_width - 40  # button width
        button_height = 50  # button height
        button_x = self.screen_width - self.control_panel_width + 20
        button_y = 50

        # Add buttons to the panel
        self.buttons.append(Button(button_x, button_y, button_width, button_height, "Start", (50, 86, 50), self.start_simulation))
        self.buttons.append(Button(button_x, button_y + 60, button_width, button_height, "Stop", (211, 171, 130), self.stop_simulation))
        self.buttons.append(Button(button_x, button_y + 120, button_width, button_height, "Reset", (123, 169, 191), self.reset))

    def stop_simulation(self):
        self.screen.simulation.stop_simulation()

    def start_simulation(self):
        self.screen.simulation.start_simulation()

    def reset(self):
        pass

    def draw_buttons(self, screen, control_panel_width):
        button_width = control_panel_width - 40
        button_height = 50
        button_x = self.screen_width - control_panel_width + 20
        button_y = 50

        pygame.draw.rect(screen, (50, 86, 50), (button_x, button_y, button_width, button_height))
        pygame.draw.rect(screen, (211, 171, 130), (button_x, button_y + 60, button_width, button_height))
        pygame.draw.rect(screen, (123, 169, 191), (button_x, button_y + 120, button_width, button_height))

        font = pygame.font.Font(None, 36)
        text_start = font.render("Start", True, (255, 255, 255))
        text_stop = font.render("Stop", True, (255, 255, 255))
        text_reset = font.render("Reset", True, (255, 255, 255))

        screen.blit(text_start, (button_x + 10, button_y + 10))
        screen.blit(text_stop, (button_x + 10, button_y + 70))
        screen.blit(text_reset, (button_x + 10, button_y + 130))
import pygame 

class Button(): 
    def __init__(self, x, y, width, height, text, color,action=None):
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
        self.font = pygame.font.Font(None, 36)  #default font & size 
        self.action = action

    
    def draw_button(self, screen):     #Draw the button on the screen.
        
        current_color = self.color
        pygame.draw.rect(screen, current_color, self.rect) # dwaw the button
        
        #button text
        text_surface = self.font.render(self.text, True, (255, 255, 255))  #white text
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def trigger(self, event):
        #Check if the button is clicked and trigger its action.
        if event.type == pygame.MOUSEBUTTONDOWN:   #Mouse click?
            if self.rect.collidepoint(event.pos):  #Mouse click within button?
                if self.action:                    #If there is an action,...
                    self.action()                  #...trigger it.
    

class GUI(): 
    def __init__(self, screen, screen_width, screen_height, control_panel_width):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.control_panel_width = control_panel_width
        self.buttons = []
        self.buttons_for_panel() 
        
    def buttons_for_panel(self):
        #make buttons to the control panel
        start_b = self.screen_width + 20  #X-position in the control panel
        button_width = self.control_panel_width - 40   #button width
        button_height = 50                             #button height           

        #buttons
        self.buttons.append(Button(start_b, 50, button_width, button_height, "Start", (0, 200, 0), self.start_simulation))
        self.buttons.append(Button(start_b, 120, button_width, button_height, "Pause", (200, 0, 0), self.pause_simulation))
        self.buttons.append(Button(start_b, 190, button_width, button_height, "Reset", (0, 0, 200), self.reset))

     
    def board(self):
        #Draw the main game board
        pygame.draw.rect(self.screen, (30, 30, 30), (0, 0, self.screen_width, self.screen_height))
    
    
    def draw_control_panel(self):
        #this is the bar where you can adjust color and interaction. it has buttons
        pygame.draw.rect(self.screen, (20, 20, 20), (self.screen_width, 0, self.control_panel_width, self.screen_height))  #control panel
        for button in self.buttons:
            button.draw_button(self.screen)   #draw rthe buttons in buttons list
            
    def handle_triggers(self, event):
        #Handle triggers for all buttons in the control panel.
        for button in self.buttons:
            button.trigger(event)
    
    
    #i am not sure if they are right in this class, but i still added them here
    def start_simulation(self):
        pass

    def pause_simulation(self):
        pass

    def reset(self):
        pass
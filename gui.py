import pygame 

class Button(): 
    def __init__(self, x, y, width, height, text, color):
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

    
    def draw_button(self, screen):     #Draw the button on the screen.
        
        current_color = self.color
        pygame.draw.rect(screen, current_color, self.rect) # dwaw the button
        
        #button text
        text_surface = self.font.render(self.text, True, (255, 255, 255))  #white text
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def trigger(self):
        #it should happen an action when you trigger/click the button
        pass 
    
    
    #Impoertant Buttons 
    def start_button(self, screen):
        self.text = "Start"  
        self.color = (0, 200, 0)  # Green
        self.draw_button(screen)
    
    def pause_button(self, screen): 
        self.text = "Stop"  
        self.color = (200, 0, 0)  # Red
        self.draw_button(screen)
        
    def reset_button(self, screen): 
        self.text = "Reset" 
        self.color = (0, 0, 200)  # Blue
        self.draw_button(screen)


class GUI(): 
    def __init__(self, screen, screen_width, screen_height, control_panel_width):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.control_panel_width = control_panel_width
        self.buttons = []
        self.setup_controls() 
     
    def board(self):
        #Draw the main game board
        pygame.draw.rect(self.screen, (30, 30, 30), (0, 0, self.screen_width, self.screen_height))
    
    
    def control_panel(self):
        #this is where the bar should go where you can adjust color and interaction
        pygame.draw.rect(self.screen, (0, 0, 0), (self.screen_width, 0, self.control_panel_width, self.screen_height))  # Black control panel


    

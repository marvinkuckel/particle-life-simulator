import pygame 

class Button(): 
    def __init__(self, x, y, width, height, text, color):
        """
        Initialize a button.
        x: X-coordinate of the button
        y: Y-coordinate of the button
        width: Button width
        height: Button height
        text: Text displayed on the button
        color: Default color of the button
        hover_color: Color of the button when hovered
        action: Function to trigger on button click
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
    def __init__():
        pass   
     
    def board():
        pass
    
    def control_panel():
        #this is where the bar should go where you can adjust color and interaction
        pass


'''


class ParticleLifeGUI():
    def __init__(self, canvas_size: Tuple[int, int], n_particles: int, fps=60):
        pygame.init()
        
        self.window = pygame.display.set_mode(canvas_size)
        # screen-updates/frames per second
        self.fps = fps
        self.simulation = PLSimulation(n_particles, canvas_size)
    
    def run(self):
        clock = pygame.time.Clock()
        dt = 0  # delta-time is used to make particle movements dependent on time (time since last screen update), to avoid different speeds for different fps
        
        self.running = True
        while self.running:
            self.event_loop()
            # time passed since last clock.tick()
            dt = clock.tick(self.fps) - dt
            self.draw_canvas(dt)
    
    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
            
            # if event.type == pygame.VIDEORESIZE:
            #     self.window = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        
    def draw_canvas(self, dt):
        # background
        self.window.fill(10)
        
        # update particle positions
        positions = self.simulation.step(dt)
        
        # draw updated particles on canvas
        for particle in positions:
            pygame.draw.circle(self.window, (255, 255,  255), particle, 1)
        # update screen with updated canvas
        pygame.display.update()

if __name__ == "__main__":
    app = ParticleLifeGUI(canvas_size=(800,800), n_particles=1000)
    app.run()
    '''
from typing import List, Tuple

import pygame

class InteractionsInterface:
    def __init__(self, interaction_matrix, type_colors: List[Tuple[int, int, int]], top_left: Tuple[int, int], right: int):
        """
        Serves as an interface between GUI and InteractionMatrix class.<br>
        Provides the visual representation of InteractionMatrix and the ability to alter the strength of force between particle types.
        
        params:
          interaction_matrix: InteractionMatrix object
          type_colors: list containing the colors of each type
          top_left (x, y): relative position/coordinate the matrix is drawn to
          right: x-coordinate to which the matrix extends (determining width and height of matrix)
        """
        self.interaction_matrix = interaction_matrix
        self.relative_position = top_left
        self.type_colors = type_colors
        
        # calculate how big each field has to be
        num_types = self.interaction_matrix.number_of_types
        self.field_size = (right - top_left[0]) / (num_types+1)
        
        # initiation the matrix fields
        rel_x, rel_y = top_left
        
        self.fields = {
            (i, j): pygame.Rect((rel_x + (j+1)*self.field_size, rel_y + (i+1)*self.field_size), (self.field_size, self.field_size))
            for i in range(num_types) for j in range(num_types)  # i = row; j = col
        }

    def draw(self, surface, mouse_pos):
        """Draws the whole InteractionsInterface including type-indicators and current state of InteractionMatrix
        
        params:
            surface: Pygame Surface to draw on.
            mouse_pos (x, y): to determine if mouse hovers over a field
        """
        self.__draw_type_indicators(surface)
        for field_index, field_rect in self.fields.items():
            interaction_value = self.interaction_matrix.interactions[field_index][0]
            
            if interaction_value > 0:
                # fade from black to green (attraction)
                color = (0, 255*interaction_value, 0)
            else:
                # fade from black to red (repulsion)
                color = (255*abs(interaction_value), 0, 0)
                
            pygame.draw.rect(surface, color, field_rect)
            
            # show value when mouse hovers field
            if field_rect.collidepoint(mouse_pos):
                text_surface = pygame.font.Font(None, 36).render(str(interaction_value), True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=field_rect.center)
                surface.blit(text_surface, text_rect)

    def handle_click(self, event: pygame.event.Event, adjust_by: float = 0.2):
        """Takes a mouse button event and modifies the force value of corresponding InteractionMatrix field.
        
        params:
          event: pygame.event.Event triggered by mouse click/scroll
          adjust_by: how much should the force be increased or decreased
        """
        # create a small pygame.Rect at mouse position to receive dict item with corresponding InteractionMatrix key
        if result := pygame.Rect(event.pos, (1, 1)).collidedict(self.fields, values=True):
            key = result[0]
            interaction_value = self.interaction_matrix.interactions[key][0]
            
            # event.button: 1 = left mouse button click; 2 = mouse wheel click; 3 = right mouse button click; 4 = mouse wheel up; 5 = mouse wheel down
            if event.button in (1, 4) and interaction_value < 1:
                self.interaction_matrix.interactions[key][0] = round(interaction_value + adjust_by, 2)  # prevent a force value grater than 1.0 due to float precision error
            if event.button in (3, 5) and interaction_value > -1:
                self.interaction_matrix.interactions[key][0] = round(interaction_value - adjust_by, 2)

    def __draw_type_indicators(self, surface):
        """Indicating the rows and columns of InteractionMatix with corresponding colors of particle types
        """
        rel_x, rel_y = self.relative_position
        radius = self.field_size * 0.2  # size of indicator
        spacing = self.field_size       # column width / row height
        
        # put center of indicator in the middle of each rows/cols
        rel_x, rel_y = rel_x + spacing/2, rel_y + spacing/2
        
        for i, color in enumerate(self.type_colors, start=1):
            pygame.draw.circle(surface, color, radius=radius, center=(rel_x + i*spacing, rel_y))  # column indicator
            pygame.draw.circle(surface, color, radius=radius, center=(rel_x, rel_y + i*spacing))  # row indicator
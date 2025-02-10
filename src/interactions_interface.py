from typing import List, Tuple

import pygame

class InteractionsInterface:
    def __init__(self, interaction_matrix, relative_position: Tuple[int, int], panel_width: int, padding: int, type_colors: List[Tuple[int, int, int]]):
        """
        Serves as an interface between GUI and InteractionMatrix class.<br>
        Provides the visual representation of InteractionMatrix and the ability to alter the strength of force between particle types.
        
        params:
          interaction_matrix: InteractionMatrix object
          relative_position: Coordinates of top-left corner
          panel_width: Width of control panel to determine the size of InteractionsInterface depending on padding
          padding: to make the interface smaller
          type_colors: list containing the color of each type
        """
        self.interaction_matrix = interaction_matrix
        self.relative_position = relative_position[0]+30, relative_position[1]+10
        self.type_colors = type_colors
        
        # calculate how big each field has to be
        num_types = self.interaction_matrix.number_of_types
        self.field_size = (panel_width - 2*padding) / (num_types+1)
        
        self.__initiate_fields()

    def draw(self, surface):
        """Draws the whole InteractionsInterface including type-indicators and current state of InteractionMatrix
        
        params:
            surface: Pygame Surface to draw on.
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
            
            # event.button: 1 = left mouse button click; 2 = mouse wheel click; 3 = right mouse button click
            # 4 = mouse wheel up
            if event.button == 4 and interaction_value < 1:
                self.interaction_matrix.interactions[key][0] = round(interaction_value + 0.2, 2)
            # 5 = mouse wheel down
            if event.button == 5 and interaction_value > -1:
                self.interaction_matrix.interactions[key][0] = round(interaction_value - 0.2, 2)

    def __initiate_fields(self):
        """
        Generates a dictionary containing InteractionMatrix indcices as keys, associating pygame.Rect objects serving as buttons to each field.<br>
        Pygame provides a method that returns the dict item of clicked pygame rect.
        """
        rel_x, rel_y = self.relative_position
        field_size = self.field_size
        types = self.interaction_matrix.number_of_types

        self.fields = {(i, j): pygame.Rect(rel_x + (j+1)*field_size,
                                           rel_y + (i+1)*field_size,
                                           field_size, field_size)
                       for i in range(types) for j in range(types)}
                
    def __draw_type_indicators(self, surface):
        """Indicating the rows and columns of InteractionMatix with corresponding colors of particle types
        """
        rel_x, rel_y = self.relative_position
        radius = self.field_size/2 - 30  # size of indicator
        spacing = self.field_size        # column/row size
        
        # put center of indicator in the middle of rows/cols
        rel_x, rel_y = rel_x + spacing/2, rel_y + spacing/2
        
        for i, color in enumerate(self.type_colors, start=1):
            pygame.draw.circle(surface, color, radius=radius, center=(rel_x + i*spacing, rel_y))  # column indicator
            pygame.draw.circle(surface, color, radius=radius, center=(rel_x, rel_y + i*spacing))  # row indicator
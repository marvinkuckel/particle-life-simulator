# src/interaction_matrix.py

class InteractionMatrix:
    def __init__(self, size):
        self.size = size
        self.matrix = [[0 for _ in range(size)] for _ in range(size)]

    def set_interaction(self, i, j, value):
        """Setzt den Interaktionswert zwischen Element i und j."""
        if 0 <= i < self.size and 0 <= j < self.size:
            self.matrix[i][j] = value
        else:
            raise IndexError("Index außerhalb des gültigen Bereichs.")

    def get_interaction(self, i, j):
        """Gibt den Interaktionswert zwischen Element i und j zurück."""
        if 0 <= i < self.size and 0 <= j < self.size:
            return self.matrix[i][j]
        else:
            raise IndexError("Index außerhalb des gültigen Bereichs.")

    def __repr__(self):
        """Gibt die Matrix in einer lesbaren Form zurück."""
        return '\n'.join(['\t'.join(map(str, row)) for row in self.matrix])

class Pointer:
    """A pointer object provides functionality to a board"""
    def __init__(self, board, **kwargs):
        """board is the only required parameter"""
        self.board = board
        
        # Prevents self.x assignment crashing
        self.cell = board.cells[0][0]
        self._x = 0
        self._y = 0
        # Code now runs smoothly
        self.x = kwargs.get('x', 0)
        self.y = kwargs.get('y', 0)
    
    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, x):
        # First deselect current cell
        self.cell.selected = False

        # Update x coordinate
        self._x = x % self.board.width

        # Finally select new cell
        self.cell = self.board.cells[self.y][self.x]
        self.cell.selected = True
    
    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, y):
        # First deselect current cell
        self.cell.selected = False

        # Update x coordinate
        self._y = y % self.board.width

        # Finally select new cell
        self.cell = self.board.cells[self.y][self.x]
        self.cell.selected = True
    
    def up(self, steps=1):
        # Remember that y decreases going up the board
        self.y -= steps

    def down(self, steps=1):
        self.y += steps
    
    def right(self, steps=1):
        self.x += steps
    
    def left(self, steps=1):
        self.x -= steps
    
    def xystr(self) -> str:
        """String representation of self"""
        return f'{self.x} {self.y}'
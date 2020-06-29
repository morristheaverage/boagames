from boagames.misc.customexceptions import ContentError, DimensionError
from boagames.misc import style

class Cell:
    """Default cell class"""
    
    def __init__(self, **kwargs):
        # Assign data to the rows
        # Blank by default
        self.x = kwargs.get('x')
        self.y = kwargs.get('y')

        self.width = kwargs.get('width', 1)
        self.height = kwargs.get('height', 1)

        self.selected = kwargs.get('selected', False)

        # Becomes true once data has been set
        self._full = False
        self.rows = kwargs.get('rows', [[' ' for _ in range(self.width)] for _ in range(self.height)])
        self._full = True

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = y

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width):
        if not type(width) == int or width < 0:
            raise DimensionError
        else:
            self._width = width

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height):
        if not type(height) == int or height < 0:
            raise DimensionError
        else:
            self._height = height

    @property
    def rows(self):
        # Allow for highlighting
        if self.selected:
            return [[style.HIGHLIGHT] + [row] + [style.RESET] for row in self._rows]
        else:
            return self._rows

    @rows.setter
    def rows(self, rows):
        # First check the data
        if rows == None:
            self._rows = [[' ' for _ in range(self.width)] for _ in range(self.height)]
        else:
            try:
                assert len(rows) == self.height
                assert all(len(row) >= self.width for row in rows)

                # Need implementation that recognises ANSI escape chars
                #for row in rows:
                #    assert all(len(str(c)) == 1 
                
                self._rows = rows
            except:
                raise ContentError

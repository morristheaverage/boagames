from cell import Cell
from customexceptions import *
import style

class UnitCell(Cell):
    """1x1 cell that is easier to use"""

    def __init__(self, **kwargs):
        self.value = kwargs.get('value', ' ')
        kwargs['rows'] = [[self.value]]
        kwargs['width'] = 1
        kwargs['height'] = 1

        # Determines how value is represented in rows
        self.selected = kwargs.get('selected', False)

        super().__init__(kwargs=kwargs)

    # Height and width are constant values for this class
    @property
    def width(self):
        return 1
    
    @width.setter
    def width(self, width):
        pass

    @property
    def height(self):
        return 1

    @height.setter
    def height(self, height):
        pass

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        try:
            # Only allow values that can be printed
            # with a single char - redo this
            if len(str(value)) >= 1:
                self._value = value
                if hasattr(self, 'selected') and self.selected:
                    self.rows = [[style.HIGHLIGHT, value, style.RESET]]
                else:
                    self.rows = [[value]]
            else:
                raise UnitValueError
        except AttributeError as error:
            print(dir(error))
            raise ContentError(error)
    
    @property
    def selected(self):
        return self._selected
    
    @selected.setter
    def selected(self, selected):
        self._selected = selected
        # Check value to refresh self.rows accordingly
        self.value = self.value
    

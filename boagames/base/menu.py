"""

    ┌────────────────────────┐
    │         Item 1         │
    ├────────────────────────┤
    │         Item 2         │
    ├────────────────────────┤
    │         Item 3         │
    ├────────────────────────┤
    │         Item 4         │
    ├────────────────────────┤
    │         Item 5         │
    ├────────────────────────┤
    │         Item 6         │
    ├────────────────────────┤
    │         Item 7         │
    ├────────────────────────┤
    │         Item 8         │
    ├────────────────────────┤
    │         Item 9         │
    ├────────────────────────┤
    │         Item 10        │
    └────────────────────────┘

"""


from boagames.base.nuBoard import NUBoard
from boagames.base.button import Button


class Menu(NUBoard):
    DEFAULT_BUTTON_WIDTH = 24
    DEFAULT_BUTTON_HEIGHT = 1

    DEFAULT_NUM_BUTTONS = 10

    """Class to display a menu on screen"""
    def __init__(self, **kwargs):
        # Set size of area containing buttons
        self.main_width = kwargs.get('main_width', self.DEFAULT_BUTTON_WIDTH)
        self.main_height = kwargs.get('main_height', self.DEFAULT_NUM_BUTTONS)

        # Set size of surrounding margins
        self.margin = kwargs.get('margin', 4)
        self.top = kwargs.get('top', 1)
        self.bottom = kwargs.get('bottom', 1)

        # Initialise dict to pass to base class
        nukwargs = {}
        nukwargs['width'] = self.margin + self.main_width
        nukwargs['height'] = self.top + self.main_height + self.bottom

        nukwargs['row_heights'] = [self.top] + [self.DEFAULT_BUTTON_HEIGHT for _ in range(self.main_height)] + [self.bottom]
        nukwargs['col_widths'] = [self.margin, self.main_width, self.margin]
        
        # Set contents
        self.buttons_dicts = kwargs.get(
            'buttons',
            [{'name': None, 'action': None} for _ in range(self.main_height)]
            )
        nukwargs

        # Set style data
        self._style = 'line'

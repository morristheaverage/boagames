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

import boagames.misc.usefulconstants as uc


class Menu(NUBoard):
    """Class to display a menu on screen"""
    def __init__(self, **kwargs):
        # Set size of area containing buttons
        self.main_width = kwargs.get('main_width', uc.MENU_DEFAULT_BUTTON_WIDTH)
        self.main_height = kwargs.get('main_height', uc.MENU_DEFAULT_NUM_BUTTONS)

        # Set size of surrounding margins
        self.margin = kwargs.get('margin', 4)
        self.top = kwargs.get('top', 1)
        self.bottom = kwargs.get('bottom', 1)
        
        # Set contents
        self.button_dicts = kwargs.get(
            'buttons',
            [{'name': None, 'action': None, 'target': None} for _ in range(self.main_height)]
            )
        # The cell_contents function is now determined by the list of buttons
        def cc_func_builder(names, width):
            def cc(x, y):
                if not x == 1:
                    return None
                if y == 0 or y > len(names):
                    return None
                else:
                    name = names[y-1]
                    overflow = width - len(name)
                    name += ' ' * overflow
                    return [[x for x in name]]
            return cc
        
        borderfunc = lambda x, y: False if (x != 1 or y == 0 or y > self.main_height) else True

        super().__init__(
            # Overall dimensions of underlying board
            board_width = self.margin + self.main_width,
            board_height = self.top + self.main_height + self.bottom,
            # More detailed heights of rows and columns
            row_heights = [self.top] + [uc.MENU_DEFAULT_BUTTON_HEIGHT for _ in range(self.main_height)] + [self.bottom],
            col_widths = [self.margin, self.main_width, self.margin],
            # Pass custom made content function for buttons
            cell_content = cc_func_builder([x['name'] for x in self.button_dicts], self.main_width),
            cell_bordered = borderfunc,
            border_style = 'line'
        )

        # Set style data
        self._style = 'line'

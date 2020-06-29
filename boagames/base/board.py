from boagames.misc.customexceptions import DimensionError, ContentError

import os
import time

class Board:
    """Default board class"""

    _border_styles = ['line', 'block', 'ascii', 'space', 'none']

    _border_chars = {
            'vertical_line': {'line': u'\u2502',
                              'ascii': '|',
                              'space': ' ',
                              'none': ''},
            'horizontal_line': {'line': u'\u2500',
                              'ascii': '-',
                              'space': ' ',
                              'none': ''},
            'plus': {'line': u'\u253c',
                     'ascii': '+',
                     'space': ' '},
            'top_half_vertical_line': {'line': u'\u2575',
                                        'ascii': "'",
                                        'space': ' ',
                                        'none': ''},
            'bottom_half_vertical_line': {'line': u'\u2577',
                                        'ascii': ',',
                                        'space': ' ',
                                        'none': ''},
            'left_up_line': {'line': u'\u2518',
                             'ascii': '/',
                             'space': ' ',
                             'none': ''},
            'right_up_line': {'line': u'\u2514',
                              'ascii': '\\',
                              'space': ' ',
                              'none': ''},
            'right_down_line': {'line': u'\u250c',
                             'ascii': '/',
                             'space': ' ',
                             'none': ''},
            'left_down_line': {'line': u'\u2510',
                             'ascii': '\\',
                             'space': ' ',
                             'none': ''},
            'vert_0': {
                'line': ' ',
                'block': ' ',
                'ascii': ' ',
                'space': ' ',
                'none': ''
                },
            'vert_1': {
                'line': u'\u2502',
                'block': u'\u258C',
                'ascii': '|',
                'space': ' ',
                'none': ''
                },
            'vert_2': {
                'line': u'\u2502',
                'block': u'\u2590',
                'ascii': '|',
                'space': ' ',
                'none': ''
                },
            'vert_3': {
                'line': u'\u2502',
                'block': u'\u2588',
                'ascii': '|',
                'space': ' ',
                'none': ''
                },
            'horiz_0': {
                'line': ' ',
                'block': ' ',
                'ascii': ' ',
                'space': ' ',
                'none': ''
                },
            'horiz_1': {
                'line': u'\u2500',
                'block': u'\u2580',
                'ascii': '-',
                'space': ' ',
                'none': ''
                },
            'horiz_2': {
                'line': u'\u2500',
                'block': u'\u2584',
                'ascii': '-',
                'space': ' ',
                'none': ''
                },
            'horiz_3': {
                'line': u'\u2500',
                'block': u'\u2588',
                'ascii': '-',
                'space': ' ',
                'none': ''
                },
            'corner_0': {
                'line': ' ',
                'block': ' ',
                'ascii': ' ',
                'space': ' ',
                'none': ''
                },
            'corner_1': {
                'line': u'\u2510',
                'block': u'\u2596',
                'ascii': '\\',
                'space': ' ',
                'none': ''
                },
            'corner_2': {
                'line': u'\u250C',
                'block': u'\u2597',
                'ascii': '/',
                'space': ' ',
                'none': ''
                },
            'corner_3': {
                'line': u'\u252C',
                'block': u'\u2584',
                'ascii': '-',
                'space': ' ',
                'none': ''
                },
            'corner_4': {
                'line': u'\u2514',
                'block': u'\u259D',
                'ascii': '\\',
                'space': ' ',
                'none': ''
                },
            'corner_5': {
                'line': u'\u253C',
                'block': u'\u259E',
                'ascii': '+',
                'space': ' ',
                'none': ''
                },
            'corner_6': {
                'line': u'\u251C',
                'block': u'\u2590',
                'ascii': '|',
                'space': ' ',
                'none': ''
                },
            'corner_7': {
                'line': u'\u253C',
                'block': u'\u259F',
                'ascii': '+',
                'space': ' ',
                'none': ''
                },
            'corner_8': {
                'line': u'\u2518',
                'block': u'\u2598',
                'ascii': '/',
                'space': ' ',
                'none': ''
                },
            'corner_9': {
                'line': u'\u2524',
                'block': u'\u258C',
                'ascii': '|',
                'space': ' ',
                'none': ''
                },
            'corner_10': {
                'line': u'\u253C',
                'block': u'\u259A',
                'ascii': '+',
                'space': ' ',
                'none': ''
                },
            'corner_11': {
                'line': u'\u253C',
                'block': u'\u2599',
                'ascii': '+',
                'space': ' ',
                'none': ''
                },
            'corner_12': {
                'line': u'\u2534',
                'block': u'\u2580',
                'ascii': '-',
                'space': ' ',
                'none': ''
                },
            'corner_13': {
                'line': u'\u253C',
                'block': u'\u259B',
                'ascii': '+',
                'space': ' ',
                'none': ''
                },
            'corner_14': {
                'line': u'\u253C',
                'block': u'\u259C',
                'ascii': '+',
                'space': ' ',
                'none': ''
                },
            'corner_15': {
                'line': u'\u253C',
                'block': u'\u2588',
                'ascii': '+',
                'space': ' ',
                'none': ''
                },
            }

    def __init__(self, board_width=1, board_height=1,
                 cell_width=1, cell_height=1,
                 cell_content=lambda x, y: None,
                 border='none',
                 cell_class=None):
        """Fills out the base board"""
        
        self.width = board_width
        self.height = board_height
        
        self.cell_width = cell_width
        self.cell_height = cell_height

        self.cell_content = cell_content

        if cell_class == None:
            from cell import Cell
        else:
            Cell = cell_class

        # cell_content(x, y) will provide data for the specified cell
        self.cells = [[None for _ in range(self.width)] for _ in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                self.cells[y][x] = Cell(x=x, y=y,
                                        width=cell_width, height=cell_height,
                                        rows = cell_content(x, y))

        self.border = border
        self._drawn = 0
        self._buffer_length = 0

        # Header and Footer attributes are strings that can be used
        self.header = None
        self.footer = None

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
        return self._rows

    @rows.setter
    def rows(self, rows):
        # First check the data
        error = 'First'
        try:
            assert len(rows) >= self.height * self.cell_height
            error = 'Second'
            assert all(len(row) >= self.width * self.cell_width for row in rows)

            # Need implementation that recognises ANSI escape chars
            #for row in rows:
            #    assert all(len(str(c)) == 1 
            
            self._rows = rows
        except AssertionError:
            raise ContentError(error)
    
    @property
    def border(self):
        return self._border
    
    @border.setter
    def border(self, border):
        assert border in Board._border_styles
        self._border = border
            

    # Base event handler classes to pass to listener
    def on_key_press(self, key):
        pass

    def on_key_release(self, key):
        pass

    def on_mouse_event(self, event):
        pass


    # Base render methods
    def draw(self):
        """Draws each row of cells in turn"""
        # Call update_frame_buffer()
        self.update_frame_buffer()
        # New frame is now stored in self.rows
        self.clear()
        # Screen has now been cleared
        self.refresh()
        # New frame has been drawn along
        # with header and footer if any exist
    
        

    def clear(self):
        """Wipes screen after previous draw"""
        os.system('cls')
        self._drawn = 0

    def refresh(self):
        if self.header:
            print(self.header)
        for row in self.rows:
            for c in row:
                print(c, end='')
            print()
        if self.footer:
            print(self.footer)

    def update_frame_buffer(self):
        new_frame = []

        if self._border != 'none':
            horiz_row = Board._border_chars['plus'][self._border].join([
                ''.join([Board._border_chars['horizontal_line'][self._border] for _ in range(self.cell_width)]) for _ in range(self.width)])
    
        for n, row_of_cells in enumerate(self.cells):
            # Empty string that we build into full row
            for i in range(self.cell_height):
                # Calculate row string from across all cells
                join_char = Board._border_chars['vertical_line'][self._border]
                row = join_char.join([''.join(cell.rows[i]) for cell in row_of_cells])

                # Update temp variables
                new_frame.append([c for c in row])
            
            if n < len(self.cells) - 1 and self._border != 'none':
                new_frame.append([c for c in horiz_row])
        

        self.rows = new_frame
        # No error
        return 'OK'

if __name__ == '__main__':
    """Test the render methods"""
    from pynput import keyboard
    test_board = Board(3, 3, 2, 2, lambda x, y: [[str(x + 3*y), ' '], [' ', ' ']], 'line')
    test_board.draw()
    test_board.loop = True
    def on_press(key):
        try:
            # Alphanumeric key
            if key.char != 'q':
                test_board.cells[0][0].rows[0][0] = key.char
                test_board.draw()
                print(key)
            else:
                test_board.loop = False
                return False
        except AttributeError:
            if key.name == 'left':
                test_board.cells[1][1].rows[0][0] = ' '
                test_board.draw()
                print(key)
            else:
                # Stop program
                print(key.name)
                test_board.loop = False
                return False

    with keyboard.Listener(
        on_press=on_press) as listener:
        listener.join()

    while test_board.loop:
        time.sleep(1/60)
    print("End")

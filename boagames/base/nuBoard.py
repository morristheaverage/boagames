from boagames.base.cell import Cell
from boagames.base.board import Board
from boagames.misc.customexceptions import ContentError

from itertools import count
import os

class NUBoard(Board):
    """Board with non-uniform cell shapes"""
    def __init__(self, **kwargs):
        """Fills out the initial board"""
        # User must provide either arrays of cell dimensions or total board sizes
        # The other can then be generated from the one provided
        tmp_row_heights = kwargs.get('row_heights', None)
        tmp_col_widths = kwargs.get('col_widths', None)

        tmp_width = kwargs.get('board_width', None)
        tmp_height = kwargs.get('board_height', None)

        # Default case
        if not(tmp_width or tmp_height or tmp_row_heights or tmp_col_widths):
            tmp_row_heights = [1]
            tmp_col_widths = [1]
            tmp_width = 1
            tmp_height = 1
        # Use arrays
        elif not (tmp_width or tmp_height):
            tmp_height = sum(tmp_row_heights)
            tmp_width = sum(tmp_col_widths)
        # Build arrays
        elif not (tmp_row_heights or tmp_col_widths):
            tmp_row_heights = [1 for _ in range(tmp_height)]
            tmp_col_widths = [1 for _ in range(tmp_width)]
        
        # Now save values
        self.row_heights, self.col_widths, self.width, self.height = tmp_row_heights, tmp_col_widths, tmp_width, tmp_height

        self.cell_content = kwargs.get('cell_content', lambda x, y: None)

        # A function to determine if cell (x, y) has a border
        self.cell_bordered = kwargs.get('cell_bordered', lambda x, y: True)

        # cell_content(x, y) will provide data for the specified cell
        self.cells = [[None for _ in range(len(self.col_widths))] for _ in range(len(self.row_heights))]
        for y, height in enumerate(self.row_heights):
            for x, width in enumerate(self.col_widths):
                self.cells[y][x] = Cell(x=x, y=y,
                                        width=width, height=height,
                                        rows=self.cell_content(x, y))
                self.cells[y][x].bordered = self.cell_bordered(x, y)

        self.border = kwargs.get('border_style', 'none')
        
        # Private attributes
        self._drawn = 0 # Num of lines drawn
        self._buffer_length = 0

        # Header and Footer attributes are strings that can be used
        self.header = None
        self.footer = None
    
    @property
    def rows(self):
        return self._rows

    @rows.setter
    def rows(self, rows):
        # First check the data
        error = 'First'
        try:
            assert len(rows) >= sum(self.row_heights)
            error = 'Second'
            assert all(len(row) >= sum(self.col_widths) for row in rows)

            self._rows = rows
        except AssertionError: 
            print('Rows:', rows)
            print(len(rows))
            raise ContentError(error)

    
    def update_frame_buffer(self):
        """Overwrite this method due to varying cell shapes"""
        new_frame = []
        
        for n, row_of_cells, next_row in zip(count(), self.cells[:-1], self.cells[1:]):
            rows_of_chars = self.draw_row_of_cells(n, row_of_cells)
            # Update temp variables
            new_frame.extend(rows_of_chars)
            
            # Add horizontal border if appropriate
            if n < len(self.cells) - 1 and self.border != 'none':
                new_frame.append(self.draw_horiz(row_of_cells, next_row))
    
        new_frame.extend(self.draw_row_of_cells(len(self.cells) - 1, self.cells[-1]))
        self.rows = new_frame
        # No error
        return 'OK'
    
    def draw_row_of_cells(self, n, row_of_cells) -> list:
        """Helper function to update_frame_buffer
        returns a list of lists of chars"""
        # Empty list that we build into full row of cells
        return_rows = []
        vert_line = Board._border_chars['vertical_line'][self.border]
        for i in range(self.row_heights[n]):
            # Calculate row string from across all cells
            row = []
            for cell, neighbour in zip(row_of_cells[:-1], row_of_cells[1:]):
                row.extend(cell.rows[i])
                if self.border != 'none':
                    row.append(vert_line if cell.bordered or neighbour.bordered else ' ')
            row.extend(row_of_cells[-1].rows[i])
            return_rows.append(row)
        return return_rows
    
    def draw_horiz(self, top, bottom) -> list:
        """Helper function to draw horizontal borders
        Encoding for corners:   
                  1 | 2         1 | 2           | B         | 2
                ----+---- ->  ----+---- so  ----+---- = ----+---- = 10
                  4 | 3         8 | 4         B |         8 |
        
        
        """
        row = ''
        
        for i, tl, tr, br, bl in zip(count(), top[:-1], top[1:], bottom[1:], bottom[:-1]):
            left_edge_code = 1*tl.bordered + 2*bl.bordered
            corner_code = 1*tl.bordered + 2*tr.bordered + 4*br.bordered + 8*bl.bordered
            
            edge_piece = Board._border_chars[f'horiz_{left_edge_code}'][self.border]
            corner_piece = Board._border_chars[f'corner_{corner_code}'][self.border]

            row += edge_piece * self.col_widths[i]
            row += corner_piece
        
        final_edge_code = 1*top[-1].bordered + 2*bottom[-1].bordered
        last_piece = Board._border_chars[f'horiz_{final_edge_code}'][self.border]
        row += last_piece * self.col_widths[-1]

        return [c for c in row]


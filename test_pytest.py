from boagames.base.nuBoard import NUBoard

class TestNUBoard:
    # 1 Board with no parameters
    def test_default(self):
        board = NUBoard()
        board.update_frame_buffer()
        assert board.width == 1
        assert board.height == 1
        assert board.rows == [[' ']]
    
    # 2 Empty 3x3 board
    def test_empty3x3(self):
        board = NUBoard(row_heights=[1, 1, 1], col_widths=[1, 1, 1])
        board.update_frame_buffer()
        assert board.width == 3
        assert board.height == 3
        assert board.rows == [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
    
    # 3a 3x3 grid of numbers 1 to 9
    def test_numbers3x3(self):
        cc = lambda x, y: [[str((x + 1) + 3*y)]]
        board = NUBoard(row_heights=[1, 1, 1], col_widths=[1, 1, 1], cell_content=cc)
        board.update_frame_buffer()
        assert board.width == 3
        assert board.height == 3
        assert board.rows == [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]
    
    # 3b 3x3 bordered grid of numbers 1 to 9
    def test_borderednumbers3x3(self):
        cc = lambda x, y: [[str((x + 1) + 3*y)]]
        board = NUBoard(row_heights=[1, 1, 1], col_widths=[1, 1, 1], cell_content=cc, border_style='line')
        board.update_frame_buffer()
        assert board.width == 3
        assert board.height == 3
        assert board.rows == [['1', '│', '2', '│', '3'], ['─', '┼', '─', '┼', '─'], ['4', '│', '5', '│', '6'], ['─', '┼', '─', '┼', '─'], ['7', '│', '8', '│', '9']]
    
    # 3c 3x3 centre cell bordered only
    def test_centreborder3x3(self):
        cc = lambda x, y: [[str((x + 1) + 3*y)]]
        borderfunc = lambda x, y: True if x == 1 and y == 1 else False
        board = NUBoard(row_heights=[1, 1, 1], col_widths=[1, 1, 1], cell_content=cc, cell_bordered=borderfunc, border_style='line')
        board.update_frame_buffer()
        assert board.width == 3
        assert board.height == 3
        assert board.rows == [['1', ' ', '2', ' ', '3'], [' ', '┌', '─', '┐', ' '], ['4', '│', '5', '│', '6'], [' ', '└', '─', '┘', ' '], ['7', ' ', '8', ' ', '9']]
    
    

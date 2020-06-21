from state import State
from itertools import cycle
import usefulconstants as uc

class TTTState(State):
    """The state of a tic-tac-toe game"""
    def __init__(self, size=3, grid=None, moves=None):
        self.size = size
        self._turn_iter = cycle([0, 1])
        self.turn = next(self._turn_iter)
        self._tokens = ('X', 'O')
        self.next_piece = self._tokens[self.turn]
        self._X_won, self._Y_won = False, False
        # Default is an empty board
        if grid:
            self.grid = grid
        else:
            self.grid = [[None for _ in range(size)] for _ in range(size)]
            # if moves were passed they must be filled in
            if moves:
                pass

    @property
    def grid(self):
        return self._grid
    
    @grid.setter
    def grid(self, grid):
        # Correct number of rows
        assert len(grid) == self.size
        # Correct number of columns
        assert all(len(row) == self.size for row in grid)

        self._grid = grid
    
    def move(self, move, check=True):
        """Given a move 'i j' as a string"""
        coords = move.split()
        i, j, token = int(coords[0]), int(coords[1]), coords[2]
        try:
            assert self.grid[j][i] == None
            self.grid[j][i] = token
        except:
            return uc.ILLEGAL
        finally:
            if not check:
                self.turn = next(self._turn_iter)
                self.next_piece = self._tokens[self.turn]
            return uc.OK
    
    def generate_legal_moves(self):
        """Return a list of legal 'i j' moves"""
        legal_moves = []
        for j, row in enumerate(self.grid):
            for i, cell in enumerate(row):
                if cell == None:
                    legal_moves.append(f'{i} {j}')

        return legal_moves
    
    def evaluate(self):
        """Has either side won?"""
        # First check rows
        for row in self.grid:
            row_start = row[0]
            won = bool(row_start) and all(t == row_start for t in row)
            if won:
                return State.Evaluation(status = uc.WON, player = self._tokens.index(row_start))
        
        # Second check columns
        for x in range(self.size):
            col_start = self.grid[0][x]
            won = bool(col_start) and all(self.grid[y][x] == col_start for y in range(self.size))
            if won:
                return State.Evaluation(status = uc.WON, player = self._tokens.index(col_start))
        
        # Finally check diagonals
        main_diag = self.grid[0][0]
        off_diag = self.grid[0][-1]

        # If main diagonal OR off diagonal
        main_won = bool(main_diag) and all(self.grid[i][i] == main_diag for i in range(self.size))
        off_won = bool(off_diag) and all(self.grid[i][-1-i] == off_diag for i in range(self.size))
        if main_won:
            return State.Evaluation(status = uc.WON, player = self._tokens.index(main_diag))
        if off_won:
            return State.Evaluation(status = uc.WON, player = self._tokens.index(off_diag))
        
        # If game hasn't been won check for a draw
        for row in self.grid:
            for t in row:
                if t == None:
                    return State.Evaluation(status = uc.ONGOING, player = uc.NA)
        
        # If the game is not ongoing it is a draw
        return State.Evaluation(status = uc.DRAWN, player = uc.NA)
    
    def reset(self):    
        """Reset to default board"""
        self.grid = [[None for _ in range(self.size)] for _ in range(self.size)]
        self._turn_iter = cycle([0, 1])
        self.turn = next(self._turn_iter)
        self._tokens = ('X', 'O')
        self.next_piece = self._tokens[self.turn]
        self._X_won, self._Y_won = False, False
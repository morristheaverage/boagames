""" Tic-tac-toe
- Tom Morris

Play tic-tac-toe on an ascii board

 | |
-+-+-
 | | 
-+-+-
 | |


X| |O
-+-+-
O|X|O
-+-+-
X| |X


A board is comprised of cells. Each cell contains the data of its contents
and what to draw to screen. The board coordinates the contents of cells
according to the game state.
"""

from boagames.base.unitCell import UnitCell
from boagames.base.board import Board
from boagames.base.pointer import Pointer

from boagames.misc.customexceptions import *
from boagames.misc import keydicts as kd
from boagames.misc import usefulconstants as uc

class TicTacToeBoard(Board):
   """A board to play tic-tac-toe on"""
   def __init__(self, state, width=3, height=3, cell_content=lambda x, y: None, border='line', cell_class=UnitCell):
      super().__init__(board_width=width, board_height=height, cell_width=1, cell_height=1, cell_content=cell_content, border=border, cell_class=cell_class)

      self.state = state
      self.game_status = uc.ONGOING

      self.turn = 'X'
      self.pointer = Pointer(self, x=1, y=1)

      self.instructions = """
      Navigate around the board with the arrow keys or wasd
      Make your move by pressing the space key
      Restart the game with r
      Quit the game with q
      WARNING - do not press the enter key"""
   
   def on_key_press(self, key):
      # Define relevant key dicts and lists for reference
      move_keys = kd.BASIC_MOVE_KEYS(self)
      quit_keys = ['q']
      # move_keys = {
      #    'w': self.pointer.up,
      #    'up': self.pointer.up,
      #    'a': self.pointer.left,
      #    'left': self.pointer.left,
      #    's': self.pointer.down,
      #    'down': self.pointer.down,
      #    'd': self.pointer.right,
      #    'right': self.pointer.right
      # }
      try:
         # Alphanumeric keys have key.char
         if key.char in quit_keys:
            # Stop program
            self.game_status = uc.QUIT
            return False
         elif key.char in ['r']:
            # Restart game
            for row in self.cells:
               for cell in row:
                  cell.value = ' '
            self.state.reset()
         elif key.char in move_keys:
            move_keys[key.char]()
         else:
            # Unknown key press
            self.footer = self.instructions
      except AttributeError:
         if key.name in move_keys:
            move_keys[key.name]()
         elif key.name == 'space':
            # Attempt to place token in cell
            # Encode the move to send to the state
            token = self.state.next_piece
            move_str = self.pointer.xystr() + ' ' + token

            res = self.state.move(move_str)
            if res == uc.OK:
               # Move was good so we can update board
               self.pointer.cell.value = token
               self.footer = None

               # Did that reach a conclusive game state
               ev = self.state.evaluate()
               if not ev.status == uc.ONGOING:
                  # Game has ended
                  self.game_status = ev.status
                  # Attach relevant footer
                  self.game_status = ev.status
                  if ev.status == uc.WON:
                     self.footer = f'Player {ev.player + 1} wins'
                  elif ev.status == uc.DRAWN:
                     self.footer = f'Draw'
                  else:
                     self.footer = f'Unexpected evaluation status {ev.status}'
            elif res == uc.ILLEGAL:
               self.footer = f'{move_str} is not a legal move'
            else:
               self.footer = f'Unrecognised response code from tttstate: {res}'
            
         else:
            # Stop the program
            self.game_status = uc.QUIT
            return False
      
def play():
   """Play tic-tac-toe"""
   from pynput import keyboard
   import time
   
   from boagames.ttt.tttstate import TTTState
   
   State = TTTState()
   B = TicTacToeBoard(state=State)
   listener =  keyboard.Listener(on_press=B.on_key_press)
   listener.start()

   B.header = 'Nought and Crosses\n'
   while B.game_status == uc.ONGOING:
      time.sleep(1/60)
      B.draw()

if __name__ == '__main__':
   play()
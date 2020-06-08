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

from unitCell import UnitCell
from customexceptions import *
from board import Board
from pointer import Pointer

class TicTacToeBoard(Board):
   """A board to play tic-tac-toe on"""
   def __init__(self, width=3, height=3, cell_content=lambda x, y: None, border='line', cell_class=UnitCell):
      super().__init__(board_width=width, board_height=height, cell_width=1, cell_height=1, cell_content=cell_content, border=border, cell_class=cell_class)

      self.turn = 'X'
      self.pointer = Pointer(self, x=1, y=1)
   
   def on_key_press(self, key):
      move_keys = {
         'w': self.pointer.up,
         'up': self.pointer.up,
         'a': self.pointer.left,
         'left': self.pointer.left,
         's': self.pointer.down,
         'down': self.pointer.down,
         'd': self.pointer.right,
         'right': self.pointer.right
      }
      try:
         # Alphanumeric keys have key.char
         if key.char in ['q']:
            # Stop program
            self.running = False
            return False
         elif key.char in ['r']:
            # Restart game
            for row in self.cells:
               for cell in row:
                  cell.value = ' '
         elif key.char in move_keys:
            move_keys[key.char]()
         else:
            pass
      except AttributeError:
         if key.name in move_keys:
            move_keys[key.name]()
         elif key.name == 'space':
            current = self.pointer.cell
            if current.value == ' ':
               current.value = self.turn
               # Change player turn
               if self.turn == 'O':
                  self.turn = 'X'
               else:
                  self.turn = 'O'
         else:
            self.running = False
            return False
      

if __name__ == '__main__':
   """Play tic-tac-toe"""
   from pynput import keyboard
   import time
   B = TicTacToeBoard()
   B.running = True
   listener =  keyboard.Listener(on_press=B.on_key_press)
   listener.start()

   while B.running:
      time.sleep(1/60)
      B.draw()
   print('Game Over')
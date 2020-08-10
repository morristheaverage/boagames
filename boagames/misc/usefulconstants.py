"""Contains useful constants to help communicate information between programs
Example of use below:

import usefulconstants as uc
...
ev = state.evaluate()
if ev.status == uc.WON:
    print(f'Player {ev.player} has won!')
elif ev.status == uc.DRAWN:
    print('Game drawn')
elif ev.status == uc.ONGOING:
    # Continue processing game until conclusion reached
...

Various sets of constants will be defined
1. Game Evaluation Constants
3. Move Data
2. Misc.
"""
# 1. Game Evaluation Constants
WON = 1000
DRAWN = 500
LOST = 100
ONGOING = 0

# 2. Move Data
OK = 200
ILLEGAL = 210

# 3. Misc.
NA = -1 # As opposed to a numbered player
QUIT = 900

# 4. Menu Constants
MENU_DEFAULT_BUTTON_WIDTH = 24
MENU_DEFAULT_BUTTON_HEIGHT = 1
MENU_DEFAULT_NUM_BUTTONS = 10
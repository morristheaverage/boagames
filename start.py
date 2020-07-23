from boagames.base.menu import Menu

import os
import sys

if __name__ == '__main__':
    # Maintain a stack of programs and the child programs
    # they instantiate
    program_stack = []

    # Initial start menu is list of available games


    start_menu = Menu()
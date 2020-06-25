"""Standard key mappings for quick importing into projects"""

def BASIC_MOVE_KEYS(bwp):
    """Takes a board with pointer style object"""
    return {
        'w': bwp.pointer.up,
        'up': bwp.pointer.up,
        'a': bwp.pointer.left,
        'left': bwp.pointer.left,
        's': bwp.pointer.down,
        'down': bwp.pointer.down,
        'd': bwp.pointer.right,
        'right': bwp.pointer.right
    }
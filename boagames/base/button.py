import boagames.misc.usefulconstants as uc
from boagames.misc.customexceptions import ActionError

class Button:
    """Button class of objects that appear in menu
    
    Buttons have an assigned action that occurs when
    they are pressed. This class will provide a builtin
    set of actions that can be accessed by a dictionary.
    """
    

    def __init__(self, **kwargs):

        self.ACTION_DICT = {
            None: self.none_action,
            'play': self.play
        }
        # Set dimensions
        self.width = kwargs.get('width', uc.MENU_DEFAULT_BUTTON_WIDTH)
        self.height = kwargs.get('height', uc.MENU_DEFAULT_BUTTON_HEIGHT)

        # Set name
        self.name = kwargs.get('name')

        # Set action
        self.action = kwargs.get('action', None)
        if self.action not in self.ACTION_DICT: raise ActionError(f'Undefined action {self.action}')

        # Set target
        self.target = kwargs.get('target', None)
    
    def act(self):
        self.ACTION_DICT[self.action](self.target)
    
    def none_action(self, target):
        """Default action value"""
        pass
    
    def play(self, target: str):
        """Basic built-in action"""
        from importlib import import_module

        while True:
            module_name = 'boagames.' + target + '.game'

            try:
                game_module = import_module(module_name)
                game_module.play()
            except:
                break
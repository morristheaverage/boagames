from importlib import import_module

while True:
    game = input('Which game do you want to play?\n')
    module_name = 'boagames.' + game + '.game'

    try:
        game_module = import_module(module_name)
        game_module.play()
    except:
        print('Closing')
        break
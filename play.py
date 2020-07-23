from importlib import import_module

while True:
    game = input('Which game do you want to play?\n')
    module_name = 'boagames.games.' + game + '.game'
    print(f'importing {module_name}')

    try:
        game_module = import_module(module_name)
        game_module.play()
    except:
        print('Closing')
        break
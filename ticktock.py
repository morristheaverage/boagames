import time
from pynput import keyboard

if __name__ == '__main__':
    for _ in range(10):
        print('tick', end='\r')
        time.sleep(1)
        print('\t\ttock', end='')
        time.sleep(1)
        print('\b\b\b\b', end='\r')

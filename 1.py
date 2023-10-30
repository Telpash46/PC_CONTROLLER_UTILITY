import time

import keyboard

def disable_keyboard():
    # Список всех клавиш на клавиатуре
    keys = [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
        'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'space', 'enter',
        'esc', 'backspace', 'tab', 'caps lock', 'shift', 'ctrl', 'alt',
        'left', 'right', 'up', 'down', 'home', 'end', 'insert', 'delete',
        'page up', 'page down', 'num lock', 'scroll lock', 'print screen',
        'pause', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10',
        'f11', 'f12', 'add', 'subtract', 'decimal',"win","play/pause media",'volume up','volume down',"previous track","next track",'stop media'
    ]

    # Блокируем каждую клавишу
    for key in keys:
        keyboard.block_key(key)

# Вызываем функцию для блокировки клавиатуры
disable_keyboard()
time.sleep(30)
keyboard.unhook_all()

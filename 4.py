import ctypes

def block_mouse():
    user32 = ctypes.windll.user32
    user32.BlockInput(True)

def unblock_mouse():
    user32 = ctypes.windll.user32
    user32.BlockInput(False)

# Вызываем функцию для блокировки мыши
block_mouse()

# Ждем 30 секунд
import time
time.sleep(30)

# Вызываем функцию для разблокировки мыши
unblock_mouse()

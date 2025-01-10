# client/utils/helpers.py

import os
import platform

def clear_screen():
    """
    Clears the console screen based on the user's operating system.
    """
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

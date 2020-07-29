import keyboard

# (keybind, module name, args)
BINDS = [("ctrl+shift+x", "script", "")]

keyboard.add_hotkey("ctrl+shift+x", print, args=("fak"))
keyboard.wait()
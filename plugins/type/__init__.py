"""
Runs a command on the system
"""
import keyboard
import logging
import time

def call(pybind, args):
    logging.debug(f"Typing the following: {args}")
    time.sleep(.5)
    keyboard.write(args)
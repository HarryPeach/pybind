"""
Controls functions to do with the pybind core
"""
import threading
import logging
import keyboard

def reload_binds(pybind):
    pybind.reload_binds()

def call(pybind, args):
    if args == "reload_binds":
        reload_binds(pybind)
    elif args == "stop":
        pybind.window.quit()
        # TODO: stop tk loop
        logging.info("Gracefully stopping pybind")
    else:
        logging.warn(f"Plugin was called with invalid arguments: {args}")
    

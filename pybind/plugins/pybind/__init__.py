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
        logging.info("Gracefully stopping pybind")
        pybind.exit()
    else:
        logging.warn(f"Plugin was called with invalid arguments: {args}")
    

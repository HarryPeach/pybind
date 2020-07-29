"""
Runs a command on the system
"""
import subprocess
import logging

def call(args):
    print(f"I was called with: {args}")
    subprocess.call(args)
#!/usr/bin/env python3
"""
Run Databot Exercises

This script provides a simple command-line interface to run the Databot exercises.
"""

import os
import sys
import importlib
import argparse

def list_exercises():
    """List all available exercises"""
    exercises = [
        f[:-3] for f in os.listdir(os.path.dirname(os.path.abspath(__file__)))
        if f.endswith('.py') and f != 'run_exercise.py' and f != 'setup.py' and not f.startswith('__')
    ]
    return sorted(exercises)

def main():
    """Main function to parse arguments and run exercises"""
    parser = argparse.ArgumentParser(description='Run Databot exercises')
    parser.add_argument('exercise', nargs='?', help='Exercise to run')
    parser.add_argument('--list', action='store_true', help='List all available exercises')
    
    args = parser.parse_args()
    
    if args.list:
        print("Available exercises:")
        for i, exercise in enumerate(list_exercises(), 1):
            print(f"{i}. {exercise}")
        return
    
    if not args.exercise:
        print("Please specify an exercise to run or use --list to see available exercises")
        return
    
    try:
        # Try to import the exercise module
        module = importlib.import_module(args.exercise)
        print(f"Running {args.exercise}...")
        
        # If the module has a main function, run it
        if hasattr(module, 'main'):
            module.main()
        else:
            # Otherwise, run the module's code
            print(f"{args.exercise} loaded successfully.")
            print("This module doesn't have a main() function.")
            print("Please refer to the module's docstring for usage instructions.")
    except ModuleNotFoundError:
        print(f"Exercise '{args.exercise}' not found.")
        print("Available exercises:")
        for i, exercise in enumerate(list_exercises(), 1):
            print(f"{i}. {exercise}")

if __name__ == "__main__":
    main()
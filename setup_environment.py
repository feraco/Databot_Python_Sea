#!/usr/bin/env python3
"""
Setup script for Databot Python Sea exercises.
This script installs the required dependencies and the Databot Python library.
"""

import os
import sys
import subprocess

def install_requirements():
    """Install the required packages from requirements.txt"""
    print("Installing required packages...")
    requirements_path = os.path.join("python_exercises", "requirements.txt")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_path])
    print("Required packages installed successfully.")

def install_databot_library():
    """Install the Databot Python library in development mode"""
    print("Installing Databot Python library...")
    databot_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "databot-py")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-e", databot_dir])
    print("Databot Python library installed successfully.")

def main():
    """Main function to set up the environment"""
    print("Setting up environment for Databot Python Sea exercises...")
    
    # Install required packages
    install_requirements()
    
    # Install Databot library
    install_databot_library()
    
    print("\nEnvironment setup complete!")
    print("You can now run the Python exercises in the 'python_exercises' directory.")
    print("For example:")
    print("  ./python_exercises/run_exercise.py --list")
    print("  ./python_exercises/run_exercise.py exercise1_light_sensor_underwater")
    print("  python python_exercises/depth_led_exercise.py")

if __name__ == "__main__":
    main()
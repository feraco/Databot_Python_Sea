# Databot Python Sea Exercises

## Overview

This repository contains exercises for using the Databot with underwater ROVs. The original exercises were provided as Jupyter notebooks, but this repository now includes Python scripts that can be used instead.

## Python Scripts vs. Jupyter Notebooks

The Python scripts in the `python_exercises` directory provide several advantages over the Jupyter notebooks:

1. **Simplified Structure** - Each script is organized with clear sections and functions
2. **Reference Implementations** - Complete reference functions are provided for each challenge
3. **Easy to Modify** - Students can easily modify the scripts without dealing with notebook cells
4. **Better Code Organization** - Functions and classes are properly defined and documented
5. **Easier Debugging** - Standard Python debugging tools work better with .py files

## Getting Started

1. Make sure you have the Databot Python library installed:
   ```
   pip install -e ./databot-py
   ```

2. Explore the Python exercises in the `python_exercises` directory
3. Read the README.md file in the `python_exercises` directory for details on each exercise

## Available Exercises

1. **Databot API Overview** - Learn the basics of the Databot Python API
2. **Depth LED Exercise** - Use pressure sensor to calculate depth and provide LED feedback
3. **Light Sensor Underwater** - Detect dark areas underwater using the light sensor
4. **Temperature Profile in Water Column** - Measure temperature at different depths
5. **Pressure to Depth Log** - Convert pressure readings to depth and create a dive log
6. **Detect Movement Underwater** - Use motion sensors to detect movement patterns
7. **Rotate and Search with Magnetometer** - Use magnetometer to detect magnetic objects

## Exercise Structure

Each exercise script follows a similar structure:

1. **Configuration Functions** - Set up the Databot with the appropriate sensors
2. **Utility Functions** - Helper functions for calculations and data processing
3. **Custom Logger Class** - Extends PyDatabotSaveToFileDataCollector to process sensor data
4. **Data Collection Function** - Runs the logger to collect and save data
5. **Visualization Function** - Creates plots from the collected data
6. **Example Usage** - Shows how to use the functions in the script

## For Instructors

The Python scripts are designed to be more accessible for students while still covering all the same concepts as the original notebooks. You can:

1. Have students start with the reference implementations and make modifications
2. Remove some of the implementation details to create "fill-in-the-blank" exercises
3. Combine multiple scripts for more complex projects
4. Use the scripts as a reference for creating your own custom exercises

## Original Jupyter Notebooks

The original Jupyter notebooks are still available in the repository:

- `Databot_API_Overview_and_Exercises_With_Code.ipynb`
- `Depth_LED_Student_Exercise.ipynb`
- `Exercise1_LightSensor_Underwater.ipynb`
- `Exercise2_TempProfile_WaterColumn.ipynb`
- `Exercise3_PressureToDepth_Log.ipynb`
- `Exercise4_DetectMovementUnderwater.ipynb`
- `Exercise5_RotateAndSearch_Magnetometer.ipynb`
# Databot Python Sea

This repository contains Python exercises for using the Databot with underwater ROVs. The exercises focus on using various sensors to collect and analyze data in underwater environments.

## Repository Organization

- **python_exercises/** - Python scripts for each exercise with simplified structure
- **jupyter_notebooks/** - Original Jupyter notebooks (for reference)
- **databot-py/** - Databot Python library

## Installation

### Option 1: Automatic Setup

Run the setup script to install all dependencies and the Databot Python library:

```bash
pip install -r python_exercises/requirements.txt
pip install -e ./databot-py
```

### Option 2: All-in-One Installation

```bash
pip install -e python_exercises
```

## Getting Started

1. Connect your Databot via Bluetooth
2. Run the address scanner to save your Databot's address:
   ```python
   from databot import PyDatabot
   PyDatabot.get_databot_address(force_address_read=True)
   ```
3. Run an exercise using one of these methods:
   - Use the run_exercise.py script: `./python_exercises/run_exercise.py exercise1_light_sensor_underwater`
   - List all available exercises: `./python_exercises/run_exercise.py --list`
   - Run a specific exercise directly: `python python_exercises/depth_led_exercise.py`

## Available Exercises

The `python_exercises` directory contains the following exercises:

1. **databot_api_overview.py** - Overview of the Databot Python API with reference functions
2. **depth_led_exercise.py** - Use pressure sensor to calculate depth and provide LED feedback
3. **exercise1_light_sensor_underwater.py** - Detect dark areas underwater using the light sensor
4. **exercise2_temp_profile_water_column.py** - Measure temperature at different depths
5. **exercise3_pressure_to_depth_log.py** - Convert pressure readings to depth and create a dive log
6. **exercise4_detect_movement_underwater.py** - Use motion sensors to detect movement patterns
7. **exercise5_rotate_and_search_magnetometer.py** - Use magnetometer to detect magnetic objects

## Exercise Structure

Each exercise script follows a similar structure:

1. **Configuration Functions** - Set up the Databot with the appropriate sensors
2. **Utility Functions** - Helper functions for calculations and data processing
3. **Custom Logger Class** - Extends PyDatabotSaveToFileDataCollector to process sensor data
4. **Data Collection Function** - Runs the logger to collect and save data
5. **Visualization Function** - Creates plots from the collected data
6. **Example Usage** - Shows how to use the functions in the script

## For Students

1. Read the docstrings at the beginning of each file to understand the exercise objective
2. Look at the example usage at the bottom of each file to see how to run the exercise
3. Modify the threshold values and LED colors to experiment with different behaviors
4. Try combining multiple sensors for more complex applications

## For Instructors

The Python scripts are designed to be more accessible for students while still covering all the same concepts as the original notebooks. You can:

1. Have students start with the reference implementations and make modifications
2. Remove some of the implementation details to create "fill-in-the-blank" exercises
3. Combine multiple scripts for more complex projects
4. Use the scripts as a reference for creating your own custom exercises

## Requirements

- Python 3.6 or higher
- Bluetooth-enabled computer
- Databot device
- Required Python packages (see requirements.txt)

## License

See the LICENSE file for details.
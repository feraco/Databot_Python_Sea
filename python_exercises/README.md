# Databot Python Sea Exercises

This directory contains Python scripts that replace the Jupyter notebooks in the main repository. Each script provides a simplified framework for completing the exercises with the Databot underwater ROV.

## Files Overview

1. **databot_api_overview.py** - Overview of the Databot Python API with reference functions
2. **depth_led_exercise.py** - Use pressure sensor to calculate depth and provide LED feedback
3. **exercise1_light_sensor_underwater.py** - Detect dark areas underwater using the light sensor
4. **exercise2_temp_profile_water_column.py** - Measure temperature at different depths
5. **exercise3_pressure_to_depth_log.py** - Convert pressure readings to depth and create a dive log
6. **exercise4_detect_movement_underwater.py** - Use motion sensors to detect movement patterns
7. **exercise5_rotate_and_search_magnetometer.py** - Use magnetometer to detect magnetic objects
8. **run_exercise.py** - Command-line tool to run any exercise
9. **requirements.txt** - List of required Python packages
10. **setup.py** - Installation script for the exercises

## Installation

1. Install the required packages:
   ```
   pip install -r python_exercises/requirements.txt
   ```

2. Install the Databot Python library:
   ```
   pip install -e ./databot-py
   ```

3. Alternatively, install everything at once:
   ```
   pip install -e python_exercises
   ```

## Getting Started

1. Pair with your Databot (only needs to be done once per computer):
   ```python
   from databot import PyDatabot
   PyDatabot.get_databot_address(force_address_read=True)
   ```

2. Run any exercise using the run_exercise.py script:
   ```
   ./python_exercises/run_exercise.py exercise1_light_sensor_underwater
   ```

3. List all available exercises:
   ```
   ./python_exercises/run_exercise.py --list
   ```

4. Or run the Python files directly:
   ```
   python python_exercises/exercise1_light_sensor_underwater.py
   ```

## Exercise Structure

Each exercise script follows a similar structure:

1. **Configuration Functions** - Set up the Databot with the appropriate sensors
2. **Utility Functions** - Helper functions for calculations and data processing
3. **Custom Logger Class** - Extends PyDatabotSaveToFileDataCollector to process sensor data
4. **Data Collection Function** - Runs the logger to collect and save data
5. **Visualization Function** - Creates plots from the collected data
6. **Example Usage** - Shows how to use the functions in the script

## Completing the Exercises

Each script contains complete reference implementations, but students should be encouraged to:

1. Modify the threshold values to better suit their environment
2. Experiment with different LED color schemes
3. Add additional data processing or visualization
4. Combine multiple sensors for more complex applications
5. Create their own custom logger classes

## Example Workflow

Here's an example of how to use one of the exercise scripts:

```python
# Import the script
from exercise3_pressure_to_depth_log import *

# Configure the Databot
config = configure_pressure_sensor()

# Collect data
collect_depth_data(config, 'my_dive_log.txt', 100)

# Visualize the results
visualize_depth_log('my_dive_log.txt')

# Calculate statistics
stats = calculate_dive_statistics('my_dive_log.txt')
```
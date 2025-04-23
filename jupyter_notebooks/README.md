# Databot Python Sea Jupyter Notebooks

This directory contains the original Jupyter notebooks for the Databot underwater ROV exercises. These notebooks have been converted to Python scripts in the `python_exercises` directory for easier use.

## Available Notebooks

1. **Databot_API_Overview_and_Exercises_With_Code.ipynb** - Overview of the Databot Python API
2. **Depth_LED_Student_Exercise.ipynb** - Use pressure sensor to calculate depth and provide LED feedback
3. **Exercise1_LightSensor_Underwater.ipynb** - Detect dark areas underwater using the light sensor
4. **Exercise2_TempProfile_WaterColumn.ipynb** - Measure temperature at different depths
5. **Exercise3_PressureToDepth_Log.ipynb** - Convert pressure readings to depth and create a dive log
6. **Exercise4_DetectMovementUnderwater.ipynb** - Use motion sensors to detect movement patterns
7. **Exercise5_RotateAndSearch_Magnetometer.ipynb** - Use magnetometer to detect magnetic objects

## Using the Notebooks

To use these notebooks:

1. Install Jupyter:
   ```
   pip install jupyter
   ```

2. Install the Databot Python library:
   ```
   pip install -e ./databot-py
   ```

3. Start Jupyter:
   ```
   jupyter notebook
   ```

4. Navigate to this directory and open any of the notebooks.

## Python Scripts Alternative

For a more streamlined experience, we recommend using the Python scripts in the `python_exercises` directory instead of these notebooks. The Python scripts provide the same functionality but are easier to modify and run.
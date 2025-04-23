"""
Exercise 2: Temperature Profile in Water Column

Objective:
Measure temperature at different depths to create a temperature profile of a water column.

This Python script provides a framework for using the Databot's temperature and pressure sensors
to measure how temperature changes with depth in a body of water.
"""

from databot import DatabotConfig, DatabotLEDConfig, PyDatabot, PyDatabotSaveToFileDataCollector
import json
import matplotlib.pyplot as plt

def configure_temp_depth_sensors():
    """
    Configure the Databot to use temperature and pressure sensors.
    
    Returns:
        DatabotConfig: Configured Databot configuration
    """
    # Create a new configuration
    config = DatabotConfig()
    
    # Enable the temperature and pressure sensors
    config.Etemp1 = True  # External temperature sensor 1
    config.pressure = True  # Pressure sensor for depth calculation
    
    # Set update interval (milliseconds)
    config.refresh = 500
    
    # Get the Databot address
    config.address = PyDatabot.get_databot_address()
    
    return config

def calculate_depth(pressure):
    """
    Calculate depth from pressure.
    
    Args:
        pressure (float): Pressure in Pascals
        
    Returns:
        float: Depth in meters
    """
    # Constants
    sea_level_pressure = 101325  # Pa
    water_density = 1000  # kg/m³
    gravity = 9.8  # m/s²
    
    # Calculate depth
    pressure_difference = pressure - sea_level_pressure
    depth = pressure_difference / (water_density * gravity)
    
    return depth

def set_led_for_temperature(config, temperature):
    """
    Set the LED color based on the water temperature.
    
    Args:
        config (DatabotConfig): The Databot configuration
        temperature (float): Temperature in Celsius
        
    Returns:
        DatabotConfig: Updated configuration
    """
    # Adjust these thresholds based on your water environment
    if temperature > 25:  # Warm
        config.led1 = DatabotLEDConfig(True, 255, 0, 0)  # Red
    elif temperature > 15:  # Moderate
        config.led1 = DatabotLEDConfig(True, 255, 255, 0)  # Yellow
    else:  # Cold
        config.led1 = DatabotLEDConfig(True, 0, 0, 255)  # Blue
    
    return config

class WaterColumnLogger(PyDatabotSaveToFileDataCollector):
    """
    Custom logger that records temperature and depth data.
    """
    def process_databot_data(self, epoch, data):
        # Get temperature and pressure values
        temperature = float(data.get("external_temp_1", 0))
        pressure = float(data.get("pressure", 101325))
        
        # Calculate depth
        depth = calculate_depth(pressure)
        data['depth'] = round(depth, 2)
        
        # Set LED based on temperature
        self.databot_config = set_led_for_temperature(self.databot_config, temperature)
        
        # Add timestamp
        data['timestamp'] = epoch
        
        # Save to file
        with open(self.file_path, 'a') as f:
            f.write(json.dumps(data) + '\n')
        
        # Print status
        print(f"Depth: {depth:.2f} m | Temperature: {temperature:.2f} °C")
        
        # Increment record counter
        self.record_number += 1
        if self.number_of_records_to_collect and self.record_number >= self.number_of_records_to_collect:
            raise Exception("Data collection complete")

def collect_water_column_data(config, filename, num_records=100):
    """
    Collect temperature and depth data from the Databot and save to a file.
    
    Args:
        config (DatabotConfig): The Databot configuration
        filename (str): Name of the file to save data to
        num_records (int): Number of records to collect
        
    Returns:
        None
    """
    logger = WaterColumnLogger(config, filename, number_of_records_to_collect=num_records)
    logger.run()

def visualize_temperature_profile(filename):
    """
    Visualize the temperature profile of the water column.
    
    Args:
        filename (str): Name of the file with collected data
        
    Returns:
        None
    """
    # Lists to store data
    temperatures = []
    depths = []
    
    # Read data from file
    with open(filename, 'r') as f:
        for line in f:
            record = json.loads(line)
            temperatures.append(float(record.get("external_temp_1", 0)))
            depths.append(float(record.get("depth", 0)))
    
    # Create the plot
    plt.figure(figsize=(8, 10))
    
    # Plot temperature vs depth (inverted y-axis for depth)
    plt.scatter(temperatures, depths, c=temperatures, cmap='coolwarm')
    plt.plot(temperatures, depths, 'k-', alpha=0.3)
    
    # Add labels and title
    plt.xlabel("Temperature (°C)")
    plt.ylabel("Depth (m)")
    plt.title("Water Column Temperature Profile")
    plt.grid(True)
    
    # Invert y-axis so depth increases downward
    plt.gca().invert_yaxis()
    
    # Add colorbar
    cbar = plt.colorbar()
    cbar.set_label('Temperature (°C)')
    
    # Show the plot
    plt.show()

# Example usage
if __name__ == "__main__":
    print("Exercise 2: Temperature Profile in Water Column")
    print("To run this exercise, use the following steps:")
    print("1. config = configure_temp_depth_sensors()")
    print("2. collect_water_column_data(config, 'water_column.txt', 100)")
    print("3. visualize_temperature_profile('water_column.txt')")
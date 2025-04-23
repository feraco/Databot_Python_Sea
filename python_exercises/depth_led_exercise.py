"""
Depth Calibration with Pressure Sensor and LED Feedback

Objective:
Use the pressure sensor to calculate water depth and provide LED feedback based on depth.

This Python script provides a framework for using the Databot's pressure sensor
to calculate water depth and change the LED color based on the current depth.
"""

from databot import DatabotConfig, DatabotLEDConfig, PyDatabot, PyDatabotSaveToFileDataCollector
import json
import matplotlib.pyplot as plt

def get_databot_address():
    """
    Scan for and save the Databot's Bluetooth address.
    Only needs to be done once per computer.
    
    Returns:
        str: The Databot's Bluetooth address
    """
    return PyDatabot.get_databot_address(force_address_read=True)

def configure_pressure_sensor():
    """
    Configure the Databot to use the pressure sensor and set the LED to blue.
    
    Returns:
        DatabotConfig: Configured Databot configuration
    """
    # Create a new configuration
    config = DatabotConfig()
    
    # Enable the pressure sensor
    config.pressure = True
    
    # Set LED1 to blue
    config.led1 = DatabotLEDConfig(True, 0, 0, 255)  # Blue
    
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
    adjusted = pressure - sea_level_pressure
    depth = adjusted / (water_density * gravity)
    
    return depth

def get_led_color(depth):
    """
    Get LED color configuration based on depth.
    
    Args:
        depth (float): Depth in meters
        
    Returns:
        DatabotLEDConfig: LED configuration
    """
    if depth > 2.5:
        return DatabotLEDConfig(True, 255, 0, 0)  # Red for deep
    elif depth > 1.0:
        return DatabotLEDConfig(True, 0, 255, 0)  # Green for medium
    else:
        return DatabotLEDConfig(True, 0, 0, 255)  # Blue for shallow

class DepthFeedbackLogger(PyDatabotSaveToFileDataCollector):
    """
    Custom logger that calculates depth, sets the LED, and writes to a file.
    """
    def process_databot_data(self, epoch, data):
        # Get pressure value
        pressure = float(data.get("pressure", 101325))
        
        # Calculate depth
        depth = calculate_depth(pressure)
        data["depth"] = round(depth, 2)
        
        # Set the LED based on depth
        self.databot_config.led1 = get_led_color(depth)
        
        # Add timestamp
        data['timestamp'] = epoch
        
        # Save to file
        with open(self.file_path, 'a') as f:
            f.write(json.dumps(data) + '\n')
        
        # Print status
        print(f"Depth: {depth:.2f} m | Pressure: {pressure:.2f} Pa")
        
        # Increment record counter
        self.record_number += 1
        if self.number_of_records_to_collect and self.record_number >= self.number_of_records_to_collect:
            raise Exception("Data collection complete")

def collect_depth_data(config, filename, num_records=100):
    """
    Collect depth data from the Databot and save to a file.
    
    Args:
        config (DatabotConfig): The Databot configuration
        filename (str): Name of the file to save data to
        num_records (int): Number of records to collect
        
    Returns:
        None
    """
    logger = DepthFeedbackLogger(config, filename, number_of_records_to_collect=num_records)
    logger.run()

def visualize_depth_data(filename):
    """
    Visualize the depth data.
    
    Args:
        filename (str): Name of the file with collected data
        
    Returns:
        None
    """
    # Lists to store data
    depths = []
    timestamps = []
    
    # Read data from file
    with open(filename, 'r') as f:
        for line in f:
            record = json.loads(line)
            depths.append(record["depth"])
            timestamps.append(record["timestamp"])
    
    # Create the plot
    plt.figure(figsize=(10, 6))
    
    # Plot depth vs time
    plt.plot(timestamps, depths, label="Depth (m)")
    
    # Add labels and title
    plt.xlabel("Time (s)")
    plt.ylabel("Depth (m)")
    plt.title("ROV Dive Depth Log")
    plt.grid(True)
    plt.legend()
    
    # Show the plot
    plt.show()

# Example usage
if __name__ == "__main__":
    print("Depth Calibration with Pressure Sensor and LED Feedback")
    print("To run this exercise, use the following steps:")
    print("1. config = configure_pressure_sensor()")
    print("2. collect_depth_data(config, 'depth_log.txt', 100)")
    print("3. visualize_depth_data('depth_log.txt')")
"""
Exercise 3: Pressure to Depth Log

Objective:
Convert pressure readings to depth measurements and create a dive log.

This Python script provides a framework for using the Databot's pressure sensor
to calculate water depth and create a log of the ROV's dive profile.
"""

from databot import DatabotConfig, DatabotLEDConfig, PyDatabot, PyDatabotSaveToFileDataCollector
import json
import matplotlib.pyplot as plt

def configure_pressure_sensor():
    """
    Configure the Databot to use the pressure sensor.
    
    Returns:
        DatabotConfig: Configured Databot configuration
    """
    # Create a new configuration
    config = DatabotConfig()
    
    # Enable the pressure sensor
    config.pressure = True
    
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

def get_led_color_for_depth(depth):
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

class DepthLogger(PyDatabotSaveToFileDataCollector):
    """
    Custom logger that converts pressure to depth and provides LED feedback.
    """
    def process_databot_data(self, epoch, data):
        # Get pressure value
        pressure = float(data.get("pressure", 101325))
        
        # Calculate depth
        depth = calculate_depth(pressure)
        data['depth'] = round(depth, 2)
        
        # Set LED based on depth
        self.databot_config.led1 = get_led_color_for_depth(depth)
        
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
    logger = DepthLogger(config, filename, number_of_records_to_collect=num_records)
    logger.run()

def visualize_depth_log(filename):
    """
    Visualize the depth log.
    
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
            depths.append(float(record.get("depth", 0)))
            timestamps.append(float(record.get("timestamp", 0)))
    
    # Create the plot
    plt.figure(figsize=(10, 6))
    
    # Plot depth vs time (inverted y-axis for depth)
    plt.plot(timestamps, depths, 'b-', label="Depth")
    
    # Add labels and title
    plt.xlabel("Time (s)")
    plt.ylabel("Depth (m)")
    plt.title("ROV Dive Profile")
    plt.grid(True)
    plt.legend()
    
    # Invert y-axis so depth increases downward
    plt.gca().invert_yaxis()
    
    # Show the plot
    plt.show()

def calculate_dive_statistics(filename):
    """
    Calculate statistics from the dive log.
    
    Args:
        filename (str): Name of the file with collected data
        
    Returns:
        dict: Dive statistics
    """
    # Lists to store data
    depths = []
    
    # Read data from file
    with open(filename, 'r') as f:
        for line in f:
            record = json.loads(line)
            depths.append(float(record.get("depth", 0)))
    
    # Calculate statistics
    max_depth = max(depths) if depths else 0
    avg_depth = sum(depths) / len(depths) if depths else 0
    
    # Print statistics
    print(f"Dive Statistics:")
    print(f"  Maximum Depth: {max_depth:.2f} m")
    print(f"  Average Depth: {avg_depth:.2f} m")
    print(f"  Dive Duration: {len(depths) * 0.5:.1f} seconds")  # Assuming 500ms refresh rate
    
    return {
        "max_depth": max_depth,
        "avg_depth": avg_depth,
        "duration": len(depths) * 0.5
    }

# Example usage
if __name__ == "__main__":
    print("Exercise 3: Pressure to Depth Log")
    print("To run this exercise, use the following steps:")
    print("1. config = configure_pressure_sensor()")
    print("2. collect_depth_data(config, 'depth_log.txt', 100)")
    print("3. visualize_depth_log('depth_log.txt')")
    print("4. calculate_dive_statistics('depth_log.txt')")
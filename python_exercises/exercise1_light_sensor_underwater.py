"""
Exercise 1: Light Sensor Underwater

Objective:
Use the ambient light sensor to detect when the ROV enters a dark underwater tunnel or shaded area.

This Python script provides a framework for using the Databot's ambient light sensor
to detect changes in light levels underwater, which can indicate entering tunnels or shaded areas.
"""

from databot import DatabotConfig, DatabotLEDConfig, PyDatabot, PyDatabotSaveToFileDataCollector
import json
import matplotlib.pyplot as plt

def configure_light_sensor():
    """
    Configure the Databot to use the ambient light sensor.
    
    Returns:
        DatabotConfig: Configured Databot configuration
    """
    # Create a new configuration
    config = DatabotConfig()
    
    # Enable the ambient light sensor
    config.ambLight = True
    
    # Set update interval (milliseconds)
    config.refresh = 500
    
    # Get the Databot address
    config.address = PyDatabot.get_databot_address()
    
    return config

def set_led_for_light_level(config, lux):
    """
    Set the LED color based on the ambient light level.
    
    Args:
        config (DatabotConfig): The Databot configuration
        lux (float): Light intensity in lux
        
    Returns:
        DatabotConfig: Updated configuration
    """
    # Adjust these thresholds based on your underwater environment
    if lux > 100:  # Bright (surface or well-lit area)
        config.led1 = DatabotLEDConfig(True, 0, 255, 0)  # Green
    elif lux > 20:  # Medium (moderate depth or partial shade)
        config.led1 = DatabotLEDConfig(True, 255, 255, 0)  # Yellow
    else:  # Dark (tunnel or deep/shaded area)
        config.led1 = DatabotLEDConfig(True, 255, 0, 0)  # Red
    
    return config

class UnderwaterLightLogger(PyDatabotSaveToFileDataCollector):
    """
    Custom logger that monitors light levels and provides LED feedback.
    """
    def process_databot_data(self, epoch, data):
        # Get light value
        light = float(data.get("ambient_light_in_lux", 0))
        
        # Add a flag to indicate if we're in a dark area (tunnel)
        in_tunnel = light < 20  # Adjust this threshold as needed
        data['in_tunnel'] = in_tunnel
        
        # Set LED based on light level
        self.databot_config = set_led_for_light_level(self.databot_config, light)
        
        # Add timestamp
        data['timestamp'] = epoch
        
        # Save to file
        with open(self.file_path, 'a') as f:
            f.write(json.dumps(data) + '\n')
        
        # Print status
        status = "TUNNEL DETECTED!" if in_tunnel else "Normal light levels"
        print(f"Light: {light:.2f} lux | {status}")
        
        # Increment record counter
        self.record_number += 1
        if self.number_of_records_to_collect and self.record_number >= self.number_of_records_to_collect:
            raise Exception("Data collection complete")

def collect_light_data(config, filename, num_records=100):
    """
    Collect light sensor data from the Databot and save to a file.
    
    Args:
        config (DatabotConfig): The Databot configuration
        filename (str): Name of the file to save data to
        num_records (int): Number of records to collect
        
    Returns:
        None
    """
    logger = UnderwaterLightLogger(config, filename, number_of_records_to_collect=num_records)
    logger.run()

def visualize_light_data(filename):
    """
    Visualize the collected light data.
    
    Args:
        filename (str): Name of the file with collected data
        
    Returns:
        None
    """
    # Lists to store data
    light_values = []
    timestamps = []
    tunnel_status = []
    
    # Read data from file
    with open(filename, 'r') as f:
        for line in f:
            record = json.loads(line)
            light_values.append(float(record.get("ambient_light_in_lux", 0)))
            timestamps.append(float(record.get("timestamp", 0)))
            tunnel_status.append(record.get("in_tunnel", False))
    
    # Create the plot
    plt.figure(figsize=(10, 6))
    
    # Plot light values
    plt.plot(timestamps, light_values, label="Light (lux)")
    
    # Highlight tunnel areas
    for i, in_tunnel in enumerate(tunnel_status):
        if in_tunnel:
            plt.axvspan(timestamps[i], timestamps[i+1] if i+1 < len(timestamps) else timestamps[i], 
                        alpha=0.3, color='red')
    
    # Add labels and title
    plt.xlabel("Time (s)")
    plt.ylabel("Light (lux)")
    plt.title("Underwater Light Levels")
    plt.grid(True)
    plt.legend()
    
    # Show the plot
    plt.show()

# Example usage
if __name__ == "__main__":
    print("Exercise 1: Light Sensor Underwater")
    print("To run this exercise, use the following steps:")
    print("1. config = configure_light_sensor()")
    print("2. collect_light_data(config, 'underwater_light.txt', 100)")
    print("3. visualize_light_data('underwater_light.txt')")
"""
Databot Python API Overview

This file provides an overview of the key classes and functions in the Databot Python API.
Each section explains the purpose of an API component, followed by example code.
"""

# Import required libraries
from databot import PyDatabot, DatabotConfig, DatabotLEDConfig, PyDatabotSaveToFileDataCollector
import json

def get_databot_address():
    """
    Scan for and save the Databot's Bluetooth address.
    Only needs to be done once per computer.
    
    Returns:
        str: The Databot's Bluetooth address
    """
    return PyDatabot.get_databot_address(force_address_read=True)

def configure_databot():
    """
    Example function to configure a Databot with basic settings.
    
    Returns:
        DatabotConfig: A configured Databot configuration object
    """
    # Create a new configuration
    config = DatabotConfig()
    
    # Enable sensors
    config.pressure = True  # Atmospheric pressure
    config.gyro = True      # Gyroscope rotation
    
    # Set update interval (milliseconds)
    config.refresh = 500
    
    # Get the Databot address
    config.address = PyDatabot.get_databot_address()
    
    return config

def set_led_color(config, color="blue"):
    """
    Set the LED color on the Databot.
    
    Args:
        config (DatabotConfig): The Databot configuration
        color (str): Color name ("red", "green", "blue", "white", "off")
        
    Returns:
        DatabotConfig: Updated configuration
    """
    if color == "red":
        config.led1 = DatabotLEDConfig(True, 255, 0, 0)
    elif color == "green":
        config.led1 = DatabotLEDConfig(True, 0, 255, 0)
    elif color == "blue":
        config.led1 = DatabotLEDConfig(True, 0, 0, 255)
    elif color == "white":
        config.led1 = DatabotLEDConfig(True, 255, 255, 255)
    elif color == "off":
        config.led1 = DatabotLEDConfig(False, 0, 0, 0)
    else:
        # Default to blue
        config.led1 = DatabotLEDConfig(True, 0, 0, 255)
    
    return config

def collect_sensor_data(config, filename, num_records=50):
    """
    Collect sensor data from the Databot and save to a file.
    
    Args:
        config (DatabotConfig): The Databot configuration
        filename (str): Name of the file to save data to
        num_records (int): Number of records to collect
        
    Returns:
        None
    """
    collector = PyDatabotSaveToFileDataCollector(
        config, 
        file_name=filename, 
        number_of_records_to_collect=num_records
    )
    collector.run()

def get_led_for_light(lux):
    """
    Return an LED configuration based on light intensity.
    
    Args:
        lux (float): Light intensity in lux
        
    Returns:
        DatabotLEDConfig: LED configuration
    """
    if lux > 800:
        return DatabotLEDConfig(True, 255, 255, 255)  # White (bright)
    elif lux > 300:
        return DatabotLEDConfig(True, 0, 0, 255)      # Blue (medium)
    else:
        return DatabotLEDConfig(True, 255, 0, 0)      # Red (dark)

class WaterDensityLogger(PyDatabotSaveToFileDataCollector):
    """
    Custom logger that calculates water density from pressure and temperature.
    """
    def process_databot_data(self, epoch, data):
        pressure = float(data.get('pressure', 101325))
        temp = float(data.get('external_temp_1', 25))
        
        # Very rough estimate of water density
        density = 1000 - (temp - 4)**2 * 0.2
        data['density'] = round(density, 2)
        data['timestamp'] = epoch
        
        with open(self.file_path, 'a') as f:
            f.write(json.dumps(data) + '\n')
        
        self.record_number += 1
        if self.number_of_records_to_collect and self.record_number >= self.number_of_records_to_collect:
            raise Exception("Data collection complete")

def detect_rotation(gyro_data):
    """
    Detect if the Databot has rotated more than 30 degrees in any direction.
    
    Args:
        gyro_data (dict): Gyroscope data
        
    Returns:
        bool: True if rotation detected, False otherwise
    """
    gx = abs(float(gyro_data.get('gyro_x', 0)))
    gy = abs(float(gyro_data.get('gyro_y', 0)))
    gz = abs(float(gyro_data.get('gyro_z', 0)))
    
    if gx > 30 or gy > 30 or gz > 30:
        return True
    return False

def print_ble_config():
    """
    Print the BLE service and characteristic UUIDs.
    """
    from databot import DatabotBLEConfig
    cfg = DatabotBLEConfig()
    print('Service UUID:', cfg.service_uuid)
    print('Read UUID:', cfg.read_uuid)
    print('Write UUID:', cfg.write_uuid)

# Example usage
if __name__ == "__main__":
    print("Databot API Overview")
    print("Run the functions in this file to interact with your Databot")
    print("For example:")
    print("  config = configure_databot()")
    print("  config = set_led_color(config, 'blue')")
    print("  collect_sensor_data(config, 'data.txt', 10)")
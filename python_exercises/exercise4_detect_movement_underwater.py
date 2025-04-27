"""
Exercise 4: Detect Movement Underwater

Objective:
Use the accelerometer and gyroscope to detect and log movement patterns underwater.

This Python script provides a framework for using the Databot's motion sensors
to detect when the ROV is moving, turning, or stationary underwater.
"""

from databot import DatabotConfig, DatabotLEDConfig, PyDatabot, PyDatabotSaveToFileDataCollector
import json
import matplotlib.pyplot as plt
import numpy as np

def configure_motion_sensors():
    """
    Configure the Databot to use motion sensors.
    
    Returns:
        DatabotConfig: Configured Databot configuration
    """
    # Create a new configuration
    config = DatabotConfig()
    
    # Enable motion sensors
    config.accl = True    # Acceleration (including gravity)
    config.Laccl = True   # Linear acceleration (gravity removed)
    config.gyro = True    # Gyroscope for rotation
    
    # Also enable pressure for depth
    config.pressure = True
    
    # Set update interval (milliseconds) - faster for motion detection
    config.refresh = 200
    
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
    sea_level_pressure = 101325  # Pa
    water_density = 1000  # kg/mÂ³
    gravity = 9.8  # m/sÂ²
    
    pressure_difference = pressure - sea_level_pressure
    depth = pressure_difference / (water_density * gravity)
    
    return depth

def detect_movement(data, threshold=0.5):
    """
    Detect if the ROV is moving based on acceleration data.
    
    Args:
        data (dict): Sensor data
        threshold (float): Movement detection threshold
        
    Returns:
        bool: True if movement detected, False otherwise
    """
    # Get linear acceleration values (gravity removed)
    lx = abs(float(data.get("linear_acceleration_x", 0)))
    ly = abs(float(data.get("linear_acceleration_y", 0)))
    lz = abs(float(data.get("linear_acceleration_z", 0)))
    
    # Calculate total acceleration magnitude
    total_accel = np.sqrt(lx**2 + ly**2 + lz**2)
    
    # Return True if acceleration exceeds threshold
    return total_accel > threshold

def detect_rotation(data, threshold=15):
    """
    Detect if the ROV is rotating based on gyroscope data.
    
    Args:
        data (dict): Sensor data
        threshold (float): Rotation detection threshold (degrees/s)
        
    Returns:
        bool: True if rotation detected, False otherwise
    """
    # Get gyroscope values
    gx = abs(float(data.get("gyro_x", 0)))
    gy = abs(float(data.get("gyro_y", 0)))
    gz = abs(float(data.get("gyro_z", 0)))
    
    # Return True if any rotation axis exceeds threshold
    return gx > threshold or gy > threshold or gz > threshold

def get_led_for_movement_state(is_moving, is_rotating):
    """
    Get LED configuration based on movement state.
    
    Args:
        is_moving (bool): Whether the ROV is moving
        is_rotating (bool): Whether the ROV is rotating
        
    Returns:
        DatabotLEDConfig: LED configuration
    """
    if is_rotating:
        return DatabotLEDConfig(True, 255, 0, 255)  # Purple for rotation
    elif is_moving:
        return DatabotLEDConfig(True, 0, 255, 0)    # Green for movement
    else:
        return DatabotLEDConfig(True, 0, 0, 255)    # Blue for stationary

class MovementDetectionLogger(PyDatabotSaveToFileDataCollector):
    def process_databot_data(self, epoch, data):
        # Detect movement and rotation
        is_moving = detect_movement(data)
        is_rotating = detect_rotation(data)
        
        # Add movement state to data
        data['is_moving'] = bool(is_moving)    # ? Force pure Python bool
        data['is_rotating'] = bool(is_rotating)  # ? Force pure Python bool
        
        # Calculate depth if pressure data is available
        if 'pressure' in data:
            pressure = float(data.get("pressure", 101325))
            depth = calculate_depth(pressure)
            data['depth'] = round(depth, 2)
        
        # Set LED based on movement state
        self.databot_config.led1 = get_led_for_movement_state(is_moving, is_rotating)
        
        # Add timestamp
        data['timestamp'] = epoch
        
        # ? Clean all data to ensure it's serializable
        clean_data = {}
        for key, value in data.items():
            if isinstance(value, np.generic):
                clean_data[key] = value.item()
            else:
                clean_data[key] = value
        
        # Save to file
        with open(self.file_path, 'a') as f:
            f.write(json.dumps(clean_data) + '\n')
        
        # Print status
        state = "ROTATING" if is_rotating else ("MOVING" if is_moving else "STATIONARY")
        print(f"State: {state} | Time: {epoch:.2f}")

        # Increment record counter
        self.record_number += 1
        if self.number_of_records_to_collect and self.record_number >= self.number_of_records_to_collect:
            raise Exception("Data collection complete")

def collect_movement_data(config, filename, num_records=200):
    """
    Collect movement data from the Databot and save to a file.
    
    Args:
        config (DatabotConfig): The Databot configuration
        filename (str): Name of the file to save data to
        num_records (int): Number of records to collect
        
    Returns:
        None
    """
    logger = MovementDetectionLogger(config, filename, number_of_records_to_collect=num_records)
    logger.run()

def visualize_movement_data(filename):
    """
    Visualize the movement data.
    
    Args:
        filename (str): Name of the file with collected data
        
    Returns:
        None
    """
    # Lists to store data
    timestamps = []
    accel_x = []
    accel_y = []
    accel_z = []
    gyro_x = []
    gyro_y = []
    gyro_z = []
    moving_states = []
    rotating_states = []
    
    # Read data from file
    with open(filename, 'r') as f:
        for line in f:
            record = json.loads(line)
            timestamps.append(float(record.get("timestamp", 0)))
            
            # Acceleration data
            accel_x.append(float(record.get("linear_acceleration_x", 0)))
            accel_y.append(float(record.get("linear_acceleration_y", 0)))
            accel_z.append(float(record.get("linear_acceleration_z", 0)))
            
            # Gyroscope data
            gyro_x.append(float(record.get("gyro_x", 0)))
            gyro_y.append(float(record.get("gyro_y", 0)))
            gyro_z.append(float(record.get("gyro_z", 0)))
            
            # Movement states
            moving_states.append(record.get("is_moving", False))
            rotating_states.append(record.get("is_rotating", False))
    
    # Create the plots
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10), sharex=True)
    
    # Plot acceleration
    ax1.plot(timestamps, accel_x, 'r-', label="X")
    ax1.plot(timestamps, accel_y, 'g-', label="Y")
    ax1.plot(timestamps, accel_z, 'b-', label="Z")
    ax1.set_ylabel("Linear Acceleration (m/sÂ²)")
    ax1.set_title("ROV Movement Data")
    ax1.grid(True)
    ax1.legend()
    
    # Plot gyroscope
    ax2.plot(timestamps, gyro_x, 'r-', label="X")
    ax2.plot(timestamps, gyro_y, 'g-', label="Y")
    ax2.plot(timestamps, gyro_z, 'b-', label="Z")
    ax2.set_ylabel("Rotation Rate (Â°/s)")
    ax2.grid(True)
    ax2.legend()
    
    # Plot movement states
    for i, (moving, rotating) in enumerate(zip(moving_states, rotating_states)):
        if rotating:
            ax3.axvspan(timestamps[i], timestamps[i+1] if i+1 < len(timestamps) else timestamps[i], 
                       alpha=0.3, color='purple')
        elif moving:
            ax3.axvspan(timestamps[i], timestamps[i+1] if i+1 < len(timestamps) else timestamps[i], 
                       alpha=0.3, color='green')
    
    ax3.set_ylim(0, 1)
    ax3.set_yticks([0.25, 0.75])
    ax3.set_yticklabels(['Stationary', 'Moving'])
    ax3.set_xlabel("Time (s)")
    ax3.grid(True)
    
    plt.tight_layout()
    plt.show()

# Example usage
if __name__ == "__main__":
    print("Exercise 4: Detect Movement Underwater")
    print("To run this exercise, use the following steps:")
    config = configure_motion_sensors()
    collect_movement_data(config, 'movement_log.txt', 200)
    visualize_movement_data('movement_log.txt')

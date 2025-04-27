"""
Exercise 3: Distance and Pressure Depth Log

Objective:
Use both the Time-of-Flight (TOF) sensor and the pressure sensor to create a dive log.
This script will log distance-based depth and raw pressure readings.
"""

from databot import DatabotConfig, DatabotLEDConfig, PyDatabot, PyDatabotSaveToFileDataCollector
import json
import matplotlib.pyplot as plt
import numpy as np

def configure_sensors():
    """
    Configure the Databot to use BOTH distance (TOF) and pressure sensors.
    """
    config = DatabotConfig()
    config.Ldist = True     # Enable TOF sensor
    config.pressure = True  # Enable pressure sensor
    config.refresh = 500
    config.address = PyDatabot.get_databot_address()
    return config

def calculate_depth_from_distance(distance_cm):
    """
    Calculate depth from distance in centimeters.
    """
    return distance_cm / 100.0

def get_led_color_for_depth(depth):
    """
    Get LED color configuration based on depth.
    """
    if depth > 2.5:
        return DatabotLEDConfig(True, 255, 0, 0)  # Red for deep
    elif depth > 1.0:
        return DatabotLEDConfig(True, 0, 255, 0)  # Green for medium
    else:
        return DatabotLEDConfig(True, 0, 0, 255)  # Blue for shallow

class DepthLogger(PyDatabotSaveToFileDataCollector):
    def process_databot_data(self, epoch, data):
        # Get distance value (cm)
        distance_cm = float(data.get("distance", 0))
        # Calculate depth (meters)
        depth = calculate_depth_from_distance(distance_cm)
        data['depth'] = round(depth, 2)

        # Get pressure value if available
        pressure = float(data.get("pressure", 0))
        data['pressure'] = round(pressure, 2)

        # Set LED color based on depth
        self.databot_config.led1 = get_led_color_for_depth(depth)

        # Add timestamp
        data['timestamp'] = epoch

        # Convert NumPy types if needed
        clean_data = {}
        for key, value in data.items():
            if isinstance(value, np.bool_):
                clean_data[key] = bool(value)
            elif isinstance(value, np.generic):
                clean_data[key] = value.item()
            else:
                clean_data[key] = value

        # Save to file
        with open(self.file_path, 'a') as f:
            f.write(json.dumps(clean_data) + '\n')

        # Print status
        print(f"Depth: {depth:.2f} m | Distance: {distance_cm:.2f} cm | Pressure: {pressure:.2f} Pa")

        self.record_number += 1
        if self.number_of_records_to_collect and self.record_number >= self.number_of_records_to_collect:
            raise Exception("Data collection complete")

def collect_depth_data(config, filename, num_records=100):
    logger = DepthLogger(config, filename, number_of_records_to_collect=num_records)
    logger.run()

def visualize_depth_log(filename):
    """
    Visualize depth data based on distance readings.
    """
    depths = []
    pressures = []
    timestamps = []

    with open(filename, 'r') as f:
        for line in f:
            record = json.loads(line)
            depths.append(float(record.get("depth", 0)))
            pressures.append(float(record.get("pressure", 0)))
            timestamps.append(float(record.get("timestamp", 0)))

    plt.figure(figsize=(10, 6))
    plt.plot(timestamps, depths, 'b-', label="Depth (m)")
    plt.xlabel("Time (s)")
    plt.ylabel("Depth (meters)")
    plt.title("ROV Dive Profile (TOF Sensor)")
    plt.grid(True)
    plt.legend()
    plt.gca().invert_yaxis()
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.plot(timestamps, pressures, 'r-', label="Pressure (Pa)")
    plt.xlabel("Time (s)")
    plt.ylabel("Pressure (Pascals)")
    plt.title("ROV Pressure Log")
    plt.grid(True)
    plt.legend()
    plt.show()

def calculate_dive_statistics(filename):
    """
    Calculate basic statistics from dive log.
    """
    depths = []

    with open(filename, 'r') as f:
        for line in f:
            record = json.loads(line)
            depths.append(float(record.get("depth", 0)))

    max_depth = max(depths) if depths else 0
    avg_depth = sum(depths) / len(depths) if depths else 0

    print("Dive Statistics:")
    print(f"  Maximum Depth: {max_depth:.2f} m")
    print(f"  Average Depth: {avg_depth:.2f} m")
    print(f"  Dive Duration: {len(depths) * 0.5:.1f} seconds")

    return {
        "max_depth": max_depth,
        "avg_depth": avg_depth,
        "duration": len(depths) * 0.5
    }

if __name__ == "__main__":
    print("Exercise 3: Distance and Pressure Depth Log")
    config = configure_sensors()
    collect_depth_data(config, 'depth_log.txt', 100)
    visualize_depth_log('depth_log.txt')
    calculate_dive_statistics('depth_log.txt')

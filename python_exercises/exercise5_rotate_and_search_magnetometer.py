"""
Exercise 5: Rotate and Search with Magnetometer

Objective:
Use the magnetometer to detect magnetic objects underwater and determine orientation.

This Python script provides a framework for using the Databot's magnetometer
to detect magnetic anomalies and determine the ROV's orientation underwater.
"""

from databot import DatabotConfig, DatabotLEDConfig, PyDatabot, PyDatabotSaveToFileDataCollector
import json
import matplotlib.pyplot as plt
import numpy as np
import math

def configure_magnetometer():
    """
    Configure the Databot to use the magnetometer and other relevant sensors.
    
    Returns:
        DatabotConfig: Configured Databot configuration
    """
    # Create a new configuration
    config = DatabotConfig()
    
    # Enable magnetometer
    config.magneto = True
    
    # Also enable gyroscope for rotation detection
    config.gyro = True
    
    # Enable pressure for depth
    config.pressure = True
    
    # Set update interval (milliseconds)
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
    water_density = 1000  # kg/m³
    gravity = 9.8  # m/s²
    
    pressure_difference = pressure - sea_level_pressure
    depth = pressure_difference / (water_density * gravity)
    
    return depth

def calculate_magnetic_field_strength(data):
    """
    Calculate the total magnetic field strength.
    
    Args:
        data (dict): Sensor data
        
    Returns:
        float: Total magnetic field strength
    """
    # Get magnetometer values
    mx = float(data.get("mag_x", 0))
    my = float(data.get("mag_y", 0))
    mz = float(data.get("mag_z", 0))
    
    # Calculate total magnetic field strength
    total_field = np.sqrt(mx**2 + my**2 + mz**2)
    
    return total_field

def calculate_heading(data):
    """
    Calculate heading (compass direction) from magnetometer data.
    
    Args:
        data (dict): Sensor data
        
    Returns:
        float: Heading in degrees (0-360)
    """
    # Get magnetometer values
    mx = float(data.get("mag_x", 0))
    my = float(data.get("mag_y", 0))
    
    # Calculate heading
    heading = math.degrees(math.atan2(my, mx))
    
    # Convert to 0-360 range
    if heading < 0:
        heading += 360
    
    return heading

def detect_magnetic_anomaly(field_strength, baseline, threshold=10):
    """
    Detect if there's a magnetic anomaly.
    
    Args:
        field_strength (float): Current magnetic field strength
        baseline (float): Baseline magnetic field strength
        threshold (float): Detection threshold percentage
        
    Returns:
        bool: True if anomaly detected, False otherwise
    """
    # Calculate percentage difference from baseline
    percent_diff = abs(field_strength - baseline) / baseline * 100
    
    # Return True if difference exceeds threshold
    return percent_diff > threshold

def get_led_for_magnetic_field(is_anomaly, heading):
    """
    Get LED configuration based on magnetic field and heading.
    
    Args:
        is_anomaly (bool): Whether a magnetic anomaly is detected
        heading (float): Heading in degrees
        
    Returns:
        DatabotLEDConfig: LED configuration
    """
    if is_anomaly:
        return DatabotLEDConfig(True, 255, 0, 0)  # Red for anomaly
    
    # Otherwise, color based on heading (compass direction)
    if 315 <= heading or heading < 45:  # North
        return DatabotLEDConfig(True, 0, 0, 255)  # Blue
    elif 45 <= heading < 135:  # East
        return DatabotLEDConfig(True, 0, 255, 0)  # Green
    elif 135 <= heading < 225:  # South
        return DatabotLEDConfig(True, 255, 255, 0)  # Yellow
    else:  # West
        return DatabotLEDConfig(True, 255, 0, 255)  # Purple

class MagnetometerLogger(PyDatabotSaveToFileDataCollector):
    """
    Custom logger that detects magnetic anomalies and tracks orientation.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.baseline_field = None
        self.calibration_count = 0
        self.calibration_sum = 0
        self.calibration_samples = 10  # Number of samples for calibration
    
    def process_databot_data(self, epoch, data):
        # Calculate magnetic field strength
        field_strength = calculate_magnetic_field_strength(data)
        data['magnetic_field_strength'] = round(field_strength, 2)
        
        # Calculate heading
        heading = calculate_heading(data)
        data['heading'] = round(heading, 1)
        
        # Calibrate baseline if needed
        if self.calibration_count < self.calibration_samples:
            self.calibration_sum += field_strength
            self.calibration_count += 1
            print(f"Calibrating... {self.calibration_count}/{self.calibration_samples}")
            
            if self.calibration_count == self.calibration_samples:
                self.baseline_field = self.calibration_sum / self.calibration_samples
                print(f"Calibration complete. Baseline: {self.baseline_field:.2f}")
                data['baseline_field'] = round(self.baseline_field, 2)
        
        # Detect anomalies after calibration
        if self.baseline_field is not None:
            is_anomaly = detect_magnetic_anomaly(field_strength, self.baseline_field)
            data['magnetic_anomaly'] = is_anomaly
            
            # Set LED based on magnetic field and heading
            self.databot_config.led1 = get_led_for_magnetic_field(is_anomaly, heading)
            
            # Print status
            status = "MAGNETIC ANOMALY DETECTED!" if is_anomaly else "Normal field"
            print(f"Field: {field_strength:.2f} | Heading: {heading:.1f}° | {status}")
        
        # Calculate depth if pressure data is available
        if 'pressure' in data:
            pressure = float(data.get("pressure", 101325))
            depth = calculate_depth(pressure)
            data['depth'] = round(depth, 2)
        
        # Add timestamp
        data['timestamp'] = epoch
        
        # Save to file
        with open(self.file_path, 'a') as f:
            f.write(json.dumps(data) + '\n')
        
        # Increment record counter
        self.record_number += 1
        if self.number_of_records_to_collect and self.record_number >= self.number_of_records_to_collect:
            raise Exception("Data collection complete")

def collect_magnetometer_data(config, filename, num_records=200):
    """
    Collect magnetometer data from the Databot and save to a file.
    
    Args:
        config (DatabotConfig): The Databot configuration
        filename (str): Name of the file to save data to
        num_records (int): Number of records to collect
        
    Returns:
        None
    """
    logger = MagnetometerLogger(config, filename, number_of_records_to_collect=num_records)
    logger.run()

def visualize_magnetometer_data(filename):
    """
    Visualize the magnetometer data.
    
    Args:
        filename (str): Name of the file with collected data
        
    Returns:
        None
    """
    # Lists to store data
    timestamps = []
    field_strengths = []
    headings = []
    anomalies = []
    baseline = None
    
    # Read data from file
    with open(filename, 'r') as f:
        for line in f:
            record = json.loads(line)
            timestamps.append(float(record.get("timestamp", 0)))
            field_strengths.append(float(record.get("magnetic_field_strength", 0)))
            headings.append(float(record.get("heading", 0)))
            anomalies.append(record.get("magnetic_anomaly", False))
            
            if "baseline_field" in record and baseline is None:
                baseline = float(record.get("baseline_field", 0))
    
    # Create the plots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    
    # Plot magnetic field strength
    ax1.plot(timestamps, field_strengths, 'b-', label="Field Strength")
    if baseline:
        ax1.axhline(y=baseline, color='r', linestyle='--', label="Baseline")
    
    # Highlight anomalies
    for i, is_anomaly in enumerate(anomalies):
        if is_anomaly:
            ax1.axvspan(timestamps[i], timestamps[i+1] if i+1 < len(timestamps) else timestamps[i], 
                       alpha=0.3, color='red')
    
    ax1.set_ylabel("Magnetic Field Strength")
    ax1.set_title("Magnetometer Data")
    ax1.grid(True)
    ax1.legend()
    
    # Plot heading (compass direction)
    ax2.plot(timestamps, headings, 'g-', label="Heading")
    ax2.set_ylabel("Heading (degrees)")
    ax2.set_xlabel("Time (s)")
    ax2.set_ylim(0, 360)
    ax2.set_yticks([0, 90, 180, 270, 360])
    ax2.set_yticklabels(['N', 'E', 'S', 'W', 'N'])
    ax2.grid(True)
    ax2.legend()
    
    plt.tight_layout()
    plt.show()
    
    # Create a polar plot for heading distribution
    plt.figure(figsize=(8, 8))
    ax = plt.subplot(111, polar=True)
    
    # Convert degrees to radians for polar plot
    headings_rad = np.array(headings) * np.pi / 180
    
    # Create histogram
    bins = np.linspace(0, 2*np.pi, 37)  # 36 bins (10 degrees each)
    hist, _ = np.histogram(headings_rad, bins)
    
    # Plot
    width = 2*np.pi / 36
    bars = ax.bar(bins[:-1], hist, width=width, alpha=0.5)
    
    # Set compass directions
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)  # Clockwise
    ax.set_thetagrids([0, 90, 180, 270], ['N', 'E', 'S', 'W'])
    
    plt.title("Heading Distribution")
    plt.tight_layout()
    plt.show()

# Example usage
if __name__ == "__main__":
    print("Exercise 5: Rotate and Search with Magnetometer")
    print("To run this exercise, use the following steps:")
    print("1. config = configure_magnetometer()")
    print("2. collect_magnetometer_data(config, 'magnetometer_log.txt', 200)")
    print("3. visualize_magnetometer_data('magnetometer_log.txt')")
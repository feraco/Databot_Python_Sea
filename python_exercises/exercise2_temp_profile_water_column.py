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
    config = DatabotConfig()
    config.ambTemp = True        # Enable ambient temperature
    config.pressure = True       # Enable pressure for depth
    config.refresh = 500
    config.address = PyDatabot.get_databot_address()
    return config

def calculate_depth(pressure):
    sea_level_pressure = 101325  # Pa
    water_density = 1000         # kg/m³
    gravity = 9.8                # m/s²
    return (pressure - sea_level_pressure) / (water_density * gravity)

def set_led_for_temperature(config, temperature):
    if temperature > 25:
        config.led1 = DatabotLEDConfig(True, 255, 0, 0)    # Warm = Red
    elif temperature > 15:
        config.led1 = DatabotLEDConfig(True, 255, 255, 0)  # Moderate = Yellow
    else:
        config.led1 = DatabotLEDConfig(True, 0, 0, 255)    # Cold = Blue
    return config

class AmbientTempLogger(PyDatabotSaveToFileDataCollector):
    def process_databot_data(self, epoch, data):
        temperature = float(data.get("ambient_temperature", 0))
        pressure = float(data.get("pressure", 101325))
        depth = calculate_depth(pressure)
        data['depth'] = round(depth, 2)
        data['temperature'] = round(temperature, 2)
        data['timestamp'] = epoch

        self.databot_config = set_led_for_temperature(self.databot_config, temperature)

        with open(self.file_path, 'a') as f:
            f.write(json.dumps(data) + '\n')

        print(f"Depth: {depth:.2f} m | Ambient Temp: {temperature:.2f} °C")

        self.record_number += 1
        if self.number_of_records_to_collect and self.record_number >= self.number_of_records_to_collect:
            raise Exception("Data collection complete")

def collect_water_column_data(config, filename, num_records=100):
    logger = AmbientTempLogger(config, filename, number_of_records_to_collect=num_records)
    logger.run()

def visualize_temperature_profile(filename):
    temps, depths = [], []
    with open(filename, 'r') as f:
        for line in f:
            record = json.loads(line)
            temps.append(float(record.get("temperature", 0)))
            depths.append(float(record.get("depth", 0)))

    plt.figure(figsize=(8, 10))
    plt.scatter(temps, depths, c=temps, cmap='coolwarm')
    plt.plot(temps, depths, 'k-', alpha=0.3)
    plt.xlabel("Ambient Temperature (°C)")
    plt.ylabel("Depth (m)")
    plt.title("Water Column Ambient Temperature Profile")
    plt.grid(True)
    plt.gca().invert_yaxis()
    cbar = plt.colorbar()
    cbar.set_label('Temperature (°C)')
    plt.show()

# Example usage
if __name__ == "__main__":
    print("Exercise 2: Ambient Temperature Profile in Water Column")
    config = configure_temp_depth_sensors()
    collect_water_column_data(config, 'ambient_temp_profile.txt', 100)
    visualize_temperature_profile('ambient_temp_profile.txt')

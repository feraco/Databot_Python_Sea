# Databot Python Sea Installation Guide

This guide will help you install and set up the Databot Python Sea package on your computer.

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- Bluetooth capability on your computer

## Installation Steps

### 1. Clone or Download the Repository

```bash
git clone https://github.com/feraco/Databot_Python_Sea.git
# OR download and extract the ZIP file from GitHub
```

### 2. Install the Databot Python Package

Navigate to the repository directory and install the databot package:

```bash
cd Databot_Python_Sea
pip install -e databot-py
```

This installs the databot package in development mode, which means any changes to the package will be immediately available without reinstalling.

### 3. Install Required Dependencies

Install the required dependencies:

```bash
cd python_exercises
pip install -r requirements.txt
```

### 4. Run the Setup Script

Run the setup environment script to ensure everything is properly configured:

```bash
cd ..  # Return to the main directory
python setup_environment.py
```

## Verifying Installation

To verify that the installation was successful, try running one of the example scripts:

```bash
cd python_exercises
python run_exercise.py
```

This should display a menu of available exercises. Select one to run it.

## Troubleshooting

### Import Errors

If you see errors like `ImportError: cannot import name 'DatabotConfig' from 'databot'`, make sure you've installed the databot package correctly using the `-e` flag as shown above.

### Bluetooth Connection Issues

If you have trouble connecting to the Databot:

1. Make sure your Databot is powered on
2. Ensure Bluetooth is enabled on your computer
3. Try running `python -c "from databot import PyDatabot; PyDatabot.get_databot_address(force_address_read=True)"` to force a new scan for the device

### Other Issues

If you encounter other issues, please check the following:

1. Make sure you're using Python 3.7 or higher
2. Ensure all dependencies are installed
3. Check that your Databot is charged and powered on
4. Verify that your computer's Bluetooth is working properly

## Getting Help

If you continue to experience issues, please open an issue on the GitHub repository with details about your problem, including:

- Your operating system
- Python version
- Error messages
- Steps you've taken to troubleshoot
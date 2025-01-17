#!/bin/bash

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Install Python if not already installed
if ! command_exists python3; then
    echo "Python3 not found. Installing Python3..."
    sudo apt update
    sudo apt install -y python3
else
    echo "Python3 is already installed."
fi

# Install pip if not already installed
if ! command_exists pip3; then
    echo "pip3 not found. Installing pip3..."
    sudo apt install -y python3-pip
else
    echo "pip3 is already installed."
fi

#------------------------------------------------------------------------------
# Create a Python virtual environment (named 'venv') if it doesn't already exist
if [ ! -d "venv" ]; then
    echo "Creating a virtual environment in './venv'..."
    python3 -m venv venv
else
    echo "Virtual environment 'venv' already exists."
fi

# Activate the virtual environment
echo "Activating the virtual environment..."
# shellcheck disable=SC1091
source venv/bin/activate
#------------------------------------------------------------------------------

# Run pip install commands
if [ -f setup.py ]; then
    echo "Running pip install ."
    pip install --upgrade pip setuptools wheel
    pip install . --use-pep517
else
    echo "setup.py not found, skipping pip install ."
fi

if [ -f requirements.txt ]; then
    echo "Installing requirements from requirements.txt..."
    pip install -r requirements.txt
else
    echo "requirements.txt not found."
fi

# Check if api.py is running and kill it if necessary
API_PROCESSES=$(pgrep -f api.py)
if [ -n "$API_PROCESSES" ]; then
    echo "api.py is already running. Killing processes..."
    for PID in $API_PROCESSES; do
        echo "Killing process ID: $PID"
        kill -9 "$PID"
    done
else
    echo "api.py is not running."
fi

# Run api.py in the background
if [ -f api.py ]; then
    echo "Running api.py in the background..."
    nohup python api.py > api.log 2>&1 &
else
    echo "api.py not found."
fi

# Run execute.py in the foreground
if [ -f execute.py ]; then
    echo "Running execute.py in the foreground..."
    python execute.py
else
    echo "execute.py not found."
fi

# Final message
echo "Script execution complete."

# Deactivate the virtual environment
echo "Deactivating the virtual environment..."
deactivate

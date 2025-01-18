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
if ! command_exists pipx; then
    echo "pipx not found. Installing pip3..."
    sudo apt install -y pipx
else
    echo "pipx is already installed."
fi

#----------------------------------------------
#------------------------------------------------------------------------------

# Run pip install commands
if [ -f setup.py ]; then
    echo "Running pip install ."
    pipx install setuptools wheel
    pipx install .
else
    echo "setup.py not found, skipping pip install ."
fi

if [ -f requirements.txt ]; then
    echo "Installing requirements from requirements.txt..."
    pipx install -r requirements.txt
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
    nohup python3 api.py > api.log 2>&1 &
else
    echo "api.py not found."
fi

# Run execute.py in the foreground
if [ -f execute.py ]; then
    echo "Running execute.py in the foreground..."
    python3 execute.py
else
    echo "execute.py not found."
fi

# Final message
echo "Script execution complete."

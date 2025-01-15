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

# Prompt for GITHUB_TOKEN if not already set
if [ -z "$GITHUB_TOKEN" ]; then
    read -p "Enter your GITHUB_TOKEN: " GITHUB_TOKEN
    export GITHUB_TOKEN
fi

# Prompt for GITHUB_USER if not already set
if [ -z "$GITHUB_USER" ]; then
    read -p "Enter your GITHUB_USER: " GITHUB_USER
    export GITHUB_USER
fi

# Prompt for OPENAI_API_KEY if not already set
if [ -z "$OPENAI_API_KEY" ]; then
    read -p "Enter your OPENAI_API_KEY: " OPENAI_API_KEY
    export OPENAI_API_KEY
fi

# Run pip install commands
if [ -f setup.py ]; then
    echo "Running pip install ."
    pip3 install --upgrade pip setuptools wheel
    pip3 install . --use-pep517
else
    echo "setup.py not found, skipping pip install ."
fi

if [ -f requirements.txt ]; then
    echo "Installing requirements from requirements.txt..."
    pip3 install -r requirements.txt
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
# Run api.py and execute.py
if [ -f api.py ]; then
    echo "Running api.py in the background..."
    nohup python3 api.py > api.log 2>&1 &
else
    echo "api.py not found."
fi

if [ -f execute.py ]; then
    echo "Running execute.py in the foreground..."
    python3 execute.py
else
    echo "execute.py not found."
fi

# Final message
echo "Script execution complete."

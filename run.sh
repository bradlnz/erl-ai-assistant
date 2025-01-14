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

# Prompt for environment variables
read -p "Enter your GITHUB_TOKEN: " GITHUB_TOKEN
read -p "Enter your GITHUB_USER: " GITHUB_USER
read -p "Enter your OPENAI_API_KEY: " OPENAI_API_KEY

# Export environment variables
export GITHUB_TOKEN
export GITHUB_USER
export OPENAI_API_KEY

# Run pip install commands
if [ -f setup.py ]; then
    echo "Running pip install ."
    pip3 install .
else
    echo "setup.py not found, skipping pip install ."
fi

if [ -f requirements.txt ]; then
    echo "Installing requirements from requirements.txt..."
    pip3 install -r requirements.txt
else
    echo "requirements.txt not found."
fi

# Run execute.py and api.py in separate terminals
if [ -f execute.py ]; then
    echo "Running execute.py in a new terminal..."
    gnome-terminal -x sh -c "python3 execute.py; exec bash"
else
    echo "execute.py not found."
fi

if [ -f api.py ]; then
    echo "Running api.py in a new terminal..."
    gnome-terminal -x sh -c "python3 api.py; exec bash"
else
    echo "api.py not found."
fi

# Final message
echo "Script execution complete."

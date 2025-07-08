#!/bin/bash

# Set the AssemblyAI API key as an environment variable
# Replace YOUR_ASSEMBLYAI_API_KEY with your actual API key
export ASSEMBLYAI_API_KEY="579bb999c2234de0921a01ce336d71da"

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change to the script directory to ensure relative paths work correctly
cd "$SCRIPT_DIR"

# Try to find and use Python executable
if command -v python3 &> /dev/null; then
    echo "Using Python executable: python3"
    python3 process_videos.py
elif command -v python &> /dev/null; then
    echo "Using Python executable: python"
    python process_videos.py
elif command -v py &> /dev/null; then
    echo "Using Python executable: py"
    py process_videos.py
else
    echo "Error: Python not found. Please install Python or add it to your PATH."
    exit 1
fi

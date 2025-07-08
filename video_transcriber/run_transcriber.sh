#!/bin/bash

# Set API keys as environment variables
export ASSEMBLYAI_API_KEY="579bb999c2234de0921a01ce336d71da"
export GEMINI_API_KEY="AIzaSyAvueAi6yz3U8sKVi9stsdbC7a31Ce6uGI"

echo "Audio Learning Article - Enhanced Video Transcriber"
echo "==================================================="
echo "Features: Video transcription + AI learning article generation"
echo ""

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
    echo ""
    echo "Required Python packages:"
    echo "- assemblyai"
    echo "- google-generativeai"
    echo "- pydub (optional)"
    echo ""
    echo "Install with: pip install assemblyai google-generativeai pydub"
    exit 1
fi

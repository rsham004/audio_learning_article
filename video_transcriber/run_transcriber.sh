#!/bin/bash

echo "Audio Learning Article - Enhanced Video Transcriber"
echo "==================================================="
echo "Features: Video transcription + AI learning article generation"
echo ""

# Check if API keys are set as environment variables
if [ -z "$ASSEMBLYAI_API_KEY" ]; then
    echo "ERROR: ASSEMBLYAI_API_KEY environment variable is not set."
    echo "Please set your AssemblyAI API key as an environment variable:"
    echo "  export ASSEMBLYAI_API_KEY=\"your_assemblyai_api_key_here\""
    echo ""
    echo "Or add it to your ~/.bashrc or ~/.zshrc file."
    exit 1
fi

if [ -z "$GEMINI_API_KEY" ]; then
    echo "ERROR: GEMINI_API_KEY environment variable is not set."
    echo "Please set your Google Gemini API key as an environment variable:"
    echo "  export GEMINI_API_KEY=\"your_gemini_api_key_here\""
    echo ""
    echo "Or add it to your ~/.bashrc or ~/.zshrc file."
    exit 1
fi

echo "✓ API keys found in environment variables"
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

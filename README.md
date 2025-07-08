# Audio Learning Article

A Python-based video transcription tool that converts MP4 videos to markdown transcripts using AssemblyAI's speech-to-text API.

## Features

- **Automatic Video Processing**: Monitors input folder for new MP4 files
- **Audio Extraction**: Converts MP4 videos to MP3 audio (with fallback for direct video transcription)
- **AI Transcription**: Uses AssemblyAI for high-quality speech-to-text conversion
- **Markdown Output**: Generates clean markdown files with transcripts
- **File Management**: Automatically moves processed videos to archive folder
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Error Handling**: Graceful handling of missing dependencies and API errors

## Directory Structure

```
audio_learning_article/
├── video_transcriber/
│   ├── InputVideos/           # Place MP4 files here for processing
│   │   └── Processed/         # Processed videos are moved here
│   ├── OutputMarkdown/        # Generated markdown transcripts
│   ├── Scripts/               # Additional scripts (if any)
│   ├── process_videos.py      # Main Python script
│   ├── run_transcriber.bat    # Windows batch file runner
│   └── run_transcriber.sh     # Bash script runner
├── .gitignore
└── README.md
```

## Prerequisites

1. **Python 3.7+** installed on your system
2. **AssemblyAI API Key** (sign up at [AssemblyAI](https://www.assemblyai.com/))
3. **Required Python packages**:
   ```bash
   pip install assemblyai pydub
   ```

## Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd audio_learning_article
   ```

2. **Install dependencies**:
   ```bash
   pip install assemblyai pydub
   ```

3. **Set up your AssemblyAI API key**:
   - Edit `run_transcriber.bat` or `run_transcriber.sh`
   - Replace `YOUR_ASSEMBLYAI_API_KEY` with your actual API key
   - Or set the environment variable `ASSEMBLYAI_API_KEY`

## Usage

### Method 1: Using the Runner Scripts

**Windows:**
```cmd
cd video_transcriber
.\run_transcriber.bat
```

**Linux/macOS:**
```bash
cd video_transcriber
bash run_transcriber.sh
```

### Method 2: Direct Python Execution

```bash
cd video_transcriber
python process_videos.py
```

### Processing Workflow

1. Place your MP4 video files in `video_transcriber/InputVideos/`
2. Run the transcriber using one of the methods above
3. The script will:
   - Extract audio from each MP4 file
   - Send audio to AssemblyAI for transcription
   - Generate markdown files in `OutputMarkdown/`
   - Move processed videos to `InputVideos/Processed/`
   - Clean up temporary audio files

## Configuration

### API Key Setup

You can set your AssemblyAI API key in several ways:

1. **Environment Variable** (recommended):
   ```bash
   export ASSEMBLYAI_API_KEY="your_api_key_here"
   ```

2. **Edit Runner Scripts**:
   - Modify the `ASSEMBLYAI_API_KEY` value in `run_transcriber.bat` or `run_transcriber.sh`

### Supported File Formats

- **Input**: MP4 video files
- **Output**: Markdown (.md) files
- **Temporary**: MP3 audio files (automatically cleaned up)

## Troubleshooting

### Common Issues

1. **"No module named 'pyaudioop'"**:
   - This is a known issue with Python 3.13
   - The script will fallback to direct video transcription
   - AssemblyAI can handle video files directly

2. **"Python not found"**:
   - Ensure Python is installed and added to your PATH
   - Try using `python3` instead of `python`

3. **"ASSEMBLYAI_API_KEY not set"**:
   - Make sure you've set your API key as described in the setup section

4. **Permission errors**:
   - Ensure you have write permissions in the project directory
   - On Linux/macOS, you might need to make the shell script executable:
     ```bash
     chmod +x run_transcriber.sh
     ```

### Dependencies

If you encounter issues with `pydub`, you might need additional system dependencies:

**Windows:**
- No additional dependencies required

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt-get install ffmpeg
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source. Please check the license file for details.

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review the AssemblyAI documentation
3. Create an issue in the repository

---

**Note**: This tool requires an active internet connection and a valid AssemblyAI API key to function properly.

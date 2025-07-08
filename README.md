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
│   ├── run_transcriber.sh     # Bash script runner
│   └── file_watcher.ps1       # PowerShell file watcher for automation
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

### Method 1: Manual Execution

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

**Direct Python:**
```bash
cd video_transcriber
python process_videos.py
```

### Method 2: Automated Processing with Windows Task Scheduler

For automatic processing when files are added to the input folder, you can set up a Windows Task Scheduler task:

#### Step-by-Step Setup:

1. **Open Task Scheduler**:
   - Press `Win + R`, type `taskschd.msc`, and press Enter
   - Or search for "Task Scheduler" in the Start menu

2. **Create a New Task**:
   - In the right panel, click "Create Task..."
   - Name: `Audio Learning Article Transcriber`
   - Description: `Automatically transcribe videos when added to input folder`
   - Check "Run whether user is logged on or not"
   - Check "Run with highest privileges"

3. **Configure Triggers**:
   - Go to the "Triggers" tab
   - Click "New..."
   - Begin the task: "On an event"
   - Settings:
     - Log: `System`
     - Source: `Microsoft-Windows-Kernel-File`
     - Event ID: `11` (file creation)
   - Click "OK"

4. **Configure Actions**:
   - Go to the "Actions" tab
   - Click "New..."
   - Action: "Start a program"
   - Program/script: `cmd.exe`
   - Add arguments: `/c "cd /d "D:\vscode_projects\challenges\audio_learning_article\video_transcriber" && run_transcriber.bat"`
   - **Note**: Replace the path with your actual project path
   - Click "OK"

5. **Configure Conditions** (Optional):
   - Go to the "Conditions" tab
   - Uncheck "Start the task only if the computer is on AC power" (for laptops)
   - Check "Wake the computer to run this task" if desired

6. **Configure Settings**:
   - Go to the "Settings" tab
   - Check "Allow task to be run on demand"
   - Check "Run task as soon as possible after a scheduled start is missed"
   - If task fails, restart every: `1 minute`
   - Attempt to restart up to: `3 times`

7. **Save the Task**:
   - Click "OK"
   - Enter your Windows password when prompted

#### Alternative: PowerShell File Watcher (Recommended)

For more precise and reliable file monitoring, use the included PowerShell file watcher script:

**To use the PowerShell file watcher:**
1. Open PowerShell as Administrator
2. Set execution policy (one-time setup):
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
3. Navigate to the video_transcriber folder:
   ```powershell
   cd "D:\vscode_projects\challenges\audio_learning_article\video_transcriber"
   ```
4. Run the file watcher:
   ```powershell
   .\file_watcher.ps1
   ```

**Features of the PowerShell file watcher:**
- **Smart file detection**: Waits for files to be fully copied before processing
- **File lock checking**: Ensures files aren't still being written to
- **Colored output**: Easy-to-read status messages
- **Error handling**: Graceful handling of transcription errors
- **Automatic path detection**: No need to edit paths in the script

**The file watcher will:**
- Monitor the InputVideos folder for new MP4 files
- Wait for files to be completely copied
- Automatically start transcription when ready
- Display progress and status messages
- Continue monitoring until you press Ctrl+C

### Processing Workflow

1. Place your MP4 video files in `video_transcriber/InputVideos/`
2. **Manual**: Run the transcriber using one of the methods above
3. **Automatic**: Files will be processed automatically if you've set up the scheduler
4. The script will:
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

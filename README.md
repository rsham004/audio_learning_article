# Audio Learning Article

An enhanced Python-based video transcription tool that converts MP4 videos to markdown transcripts and automatically generates comprehensive learning articles using AI.

## Features

- **🎥 Automatic Video Processing**: Monitors input folder for new MP4 files
- **🎵 Audio Extraction**: Converts MP4 videos to MP3 audio (with fallback for direct video transcription)
- **🤖 AI Transcription**: Uses AssemblyAI for high-quality speech-to-text conversion
- **📚 Learning Article Generation**: Uses Google Gemini AI to create structured educational articles
- **📝 Dual Output**: Generates both raw transcripts and enhanced learning articles
- **🗑️ Smart File Management**: Automatically deletes processed videos after successful completion
- **💰 Cost Tracking**: Monitors and logs API usage costs for both services
- **🖥️ Cross-Platform**: Works on Windows, macOS, and Linux
- **⚡ Automated Workflow**: Drop video → get transcript + learning article
- **🛡️ Error Handling**: Graceful handling of missing dependencies and API errors

## Directory Structure

```
audio_learning_article/
├── video_transcriber/
│   ├── InputVideos/           # Place MP4 files here (auto-deleted after processing)
│   ├── OutputMarkdown/        # Raw transcripts from AssemblyAI
│   ├── LearningArticles/      # Enhanced learning articles from Gemini AI
│   ├── Scripts/               # Additional scripts (if any)
│   ├── process_videos.py      # Main Python script
│   ├── article_generator.py   # Gemini AI article generation module
│   ├── run_transcriber.bat    # Windows batch file runner
│   ├── run_transcriber.sh     # Bash script runner
│   └── file_watcher.ps1       # PowerShell file watcher for automation
├── .gitignore
└── README.md
```

## Prerequisites

1. **Python 3.7+** installed on your system
2. **AssemblyAI API Key** (sign up at [AssemblyAI](https://www.assemblyai.com/))
3. **Google Gemini API Key** (sign up at [Google AI Studio](https://makersuite.google.com/))
4. **Required Python packages**:
   ```bash
   pip install assemblyai google-generativeai pydub
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

### Enhanced Processing Workflow

1. **Drop MP4 files** in `video_transcriber/InputVideos/`
2. **Choose execution method**:
   - **Manual**: Run the transcriber using one of the methods above
   - **Automatic**: Files will be processed automatically if you've set up the scheduler/file watcher
3. **The enhanced script will**:
   - ✅ Extract audio from each MP4 file
   - ✅ Send audio to AssemblyAI for transcription
   - ✅ Generate raw transcript in `OutputMarkdown/`
   - ✅ Send transcript to Google Gemini AI for article generation
   - ✅ Create structured learning article in `LearningArticles/`
   - ✅ Delete original MP4 file (only after successful completion)
   - ✅ Clean up temporary audio files
   - ✅ Log processing costs and metadata

**Output Files:**
- `OutputMarkdown/[filename].md` - Raw transcript from AssemblyAI
- `LearningArticles/[filename]_article.md` - Enhanced learning article from Gemini

**Safety Features:**
- Original video files are only deleted after BOTH transcription AND article generation succeed
- If any step fails, the original video is preserved
- Detailed error logging and cost tracking

## Configuration

### API Key Setup

You need to configure both API keys as environment variables for security:

**Method 1: Environment Variables (Recommended)**
```bash
# Linux/macOS
export ASSEMBLYAI_API_KEY="your_assemblyai_key_here"
export GEMINI_API_KEY="your_gemini_key_here"

# Windows Command Prompt
set ASSEMBLYAI_API_KEY=your_assemblyai_key_here
set GEMINI_API_KEY=your_gemini_key_here

# Windows PowerShell
$env:ASSEMBLYAI_API_KEY="your_assemblyai_key_here"
$env:GEMINI_API_KEY="your_gemini_key_here"
```

**Method 2: Add to Shell Profile (Persistent)**
```bash
# Add to ~/.bashrc, ~/.zshrc, or ~/.profile
echo 'export ASSEMBLYAI_API_KEY="your_assemblyai_key_here"' >> ~/.bashrc
echo 'export GEMINI_API_KEY="your_gemini_key_here"' >> ~/.bashrc
source ~/.bashrc
```

**Method 3: Windows System Environment Variables**
1. Open System Properties → Advanced → Environment Variables
2. Add new user variables:
   - `ASSEMBLYAI_API_KEY` = your_assemblyai_key_here
   - `GEMINI_API_KEY` = your_gemini_key_here

**⚠️ Security Note:** Never commit API keys to version control. The runner scripts now check for environment variables and will not expose your keys.

### Supported File Formats

- **Input**: MP4 video files
- **Output**: 
  - Raw transcripts: Markdown (.md) files
  - Learning articles: Enhanced markdown (.md) files with structured content
- **Temporary**: MP3 audio files (automatically cleaned up)

### Cost Management

The system tracks costs for both APIs:
- **AssemblyAI**: ~$0.37 per hour of audio
- **Google Gemini 1.5 Flash**: ~$0.075 per 1M input tokens, $0.30 per 1M output tokens
- Cost estimates are logged with each processing session

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

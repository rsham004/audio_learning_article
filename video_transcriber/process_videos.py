import os
import assemblyai as aai

# Try to import pydub, with fallback for Python 3.13 compatibility
try:
    from pydub import AudioSegment
    PYDUB_AVAILABLE = True
except ImportError as e:
    print(f"Warning: pydub import failed: {e}")
    print("Audio conversion will be skipped. Please ensure your input files are already in MP3 format.")
    PYDUB_AVAILABLE = False

# --- Configuration ---
# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FOLDER = os.path.join(SCRIPT_DIR, "InputVideos")
OUTPUT_FOLDER = os.path.join(SCRIPT_DIR, "OutputMarkdown")
PROCESSED_FOLDER = os.path.join(INPUT_FOLDER, "Processed")

# Ensure both output and processed folders exist
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

def process_video(video_path):
    video_filename = os.path.basename(video_path)
    base_name = os.path.splitext(video_filename)[0]
    
    mp3_path = os.path.join(OUTPUT_FOLDER, f"{base_name}.mp3") # Or a temp folder
    markdown_path = os.path.join(OUTPUT_FOLDER, f"{base_name}.md")

    print(f"Processing: {video_filename}")

    try:
        # 1. Convert MP4 to MP3 using pydub (if available)
        if PYDUB_AVAILABLE:
            audio = AudioSegment.from_file(video_path, format="mp4")
            audio.export(mp3_path, format="mp3")
            print(f"Extracted audio to: {mp3_path}")
            audio_file_path = mp3_path
        else:
            # If pydub is not available, try to transcribe the video file directly
            print("pydub not available, attempting to transcribe video file directly...")
            audio_file_path = video_path

        # 2. Transcribe using AssemblyAI
        aai.settings.api_key = os.environ.get("ASSEMBLYAI_API_KEY") # Get API key from environment variable
        if not aai.settings.api_key:
            print("ASSEMBLYAI_API_KEY environment variable not set. Please set it to your AssemblyAI API key.")
            return

        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio_file_path)
        
        if transcript.status == aai.TranscriptStatus.completed:
            transcript_text = transcript.text
            print("Transcribed using AssemblyAI.")
        else:
            print(f"AssemblyAI transcription failed: {transcript.error}")
            return # Stop processing this file

        # 3. Create Markdown File
        with open(markdown_path, "w", encoding="utf-8") as f:
            f.write(f"# Transcript for {video_filename}\n\n")
            f.write(transcript_text)
        print(f"Created Markdown: {markdown_path}")

        # 4. Move processed MP4 to archive
        os.rename(video_path, os.path.join(PROCESSED_FOLDER, video_filename))
        print(f"Moved {video_filename} to processed folder.")

        # Clean up temporary MP3 (only if we created one)
        if PYDUB_AVAILABLE and os.path.exists(mp3_path):
             os.remove(mp3_path)
             print(f"Removed temporary MP3: {mp3_path}")


    except Exception as e:
        print(f"Error processing {video_filename}: {e}")

def main():
    print("Checking for new video files...")
    for filename in os.listdir(INPUT_FOLDER):
        if filename.lower().endswith(".mp4"):
            video_path = os.path.join(INPUT_FOLDER, filename)
            # Ensure it's a file, not a directory
            if os.path.isfile(video_path):
                process_video(video_path)
    print("Finished checking for video files.")

if __name__ == "__main__":
    main()

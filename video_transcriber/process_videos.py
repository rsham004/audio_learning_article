import os
import assemblyai as aai
from article_generator import ArticleGenerator
from dotenv import load_dotenv  # Add dotenv import

load_dotenv()  # Load environment variables

# Try to import pydub, with fallback for Python 3.13 compatibility
try:
    from pydub import AudioSegment
    PYDUB_AVAILABLE = True
    print("✓ pydub is available for audio conversion")
except ImportError as e:
    print(f"Warning: pydub import failed: {e}")
    if "pyaudioop" in str(e) or "audioop" in str(e):
        print("This is a known issue with Python 3.13 where audioop module was removed.")
        print("MP4 to MP3 conversion will be skipped. Please use MP3 files directly or convert them manually.")
    else:
        print("Audio conversion will be skipped. Please ensure your input files are already in MP3 format.")
    PYDUB_AVAILABLE = False

# --- Configuration ---
# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FOLDER = os.path.join(SCRIPT_DIR, "InputVideos")
OUTPUT_FOLDER = os.path.join(SCRIPT_DIR, "OutputMarkdown")
LEARNING_ARTICLES_FOLDER = os.path.join(SCRIPT_DIR, "LearningArticles")

# Ensure output folders exist
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(LEARNING_ARTICLES_FOLDER, exist_ok=True)

def process_video(video_path, relative_path):
    video_filename = os.path.basename(video_path)
    base_name = os.path.splitext(video_filename)[0]
    file_extension = os.path.splitext(video_filename)[1].lower()

    # Create the same folder structure in output directories
    output_dir_markdown = os.path.join(OUTPUT_FOLDER, relative_path)
    output_dir_articles = os.path.join(LEARNING_ARTICLES_FOLDER, relative_path)
    
    os.makedirs(output_dir_markdown, exist_ok=True)
    os.makedirs(output_dir_articles, exist_ok=True)

    mp3_path = os.path.join(output_dir_markdown, f"{base_name}.mp3")
    markdown_path = os.path.join(output_dir_markdown, f"{base_name}.md")
    article_path = os.path.join(output_dir_articles, f"{base_name}_article.md")

    print(f"Processing: {os.path.join(relative_path, video_filename)}")
    print("=" * 50)

    try:
        # 1. Handle audio extraction based on file type
        print("Step 1: Audio preparation...")
        
        # If it's already an MP3 file, use it directly
        if file_extension == ".mp3":
            print("✓ Input is already MP3 format, using directly.")
            audio_file_path = video_path
        elif PYDUB_AVAILABLE and file_extension == ".mp4":
            # Convert MP4 to MP3 using pydub
            try:
                audio = AudioSegment.from_file(video_path)
                audio.export(mp3_path, format="mp3")
                print(f"✓ Extracted audio to: {mp3_path}")
                audio_file_path = mp3_path
            except (OSError, IOError) as e:
                print(f"Error converting video to MP3: {e}")
                print("Ensure ffmpeg is installed and in your PATH. Falling back to original video.")
                audio_file_path = video_path
            except Exception as e:
                print(f"Unexpected error during audio conversion: {e}")
                print("Falling back to original video file.")
                audio_file_path = video_path
        else:
            print("⚠ pydub not available or unsupported format, attempting to transcribe file directly...")
            audio_file_path = video_path

        # 2. Transcribe using AssemblyAI
        print("Step 2: Transcription...")
        aai.settings.api_key = os.environ.get("ASSEMBLYAI_API_KEY")
        if not aai.settings.api_key:
            print("❌ ASSEMBLYAI_API_KEY environment variable not set. Please set it to your AssemblyAI API key.")
            return False

        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio_file_path)
        
        if transcript.status == aai.TranscriptStatus.completed:
            transcript_text = transcript.text or ""
            if not transcript_text:
                print("❌ Transcription completed but no text was returned.")
                return False
            print("✓ Transcribed using AssemblyAI.")
        else:
            print(f"❌ AssemblyAI transcription failed: {transcript.error}")
            return False

        # 3. Create Markdown Transcript File
        print("Step 3: Creating transcript file...")
        with open(markdown_path, "w", encoding="utf-8") as f:
            f.write(f"# Transcript for {video_filename}\n\n")
            f.write(transcript_text)
        print(f"✓ Created transcript: {markdown_path}")

        # 4. Generate Learning Article using Gemini
        print("Step 4: Generating learning article...")
        try:
            # Initialize article generator
            article_generator = ArticleGenerator()
            
            # Generate the learning article
            article_content, metadata = article_generator.generate_article(transcript_text, video_filename)
            
            # Save the article
            article_generator.save_article(article_content, article_path, metadata)
            print(f"✓ Created learning article: {article_path}")
            
        except Exception as e:
            print(f"❌ Error generating learning article: {e}")
            print("⚠ Transcript saved, but article generation failed. Keeping original video file.")
            return False

        # 5. Clean up temporary MP3 (only if we created one and it's not the original file)
        if PYDUB_AVAILABLE and file_extension == ".mp4" and os.path.exists(mp3_path):
            os.remove(mp3_path)
            print(f"✓ Removed temporary MP3: {mp3_path}")

        # 6. Delete original video file (only after successful completion)
        print("Step 5: Cleaning up...")
        try:
            os.remove(video_path)
            print(f"✓ Deleted original video file: {video_filename}")
        except Exception as e:
            print(f"⚠ Warning: Could not delete original video file: {e}")

        print("🎉 Processing completed successfully!")
        print(f"📄 Transcript: {os.path.basename(markdown_path)}")
        print(f"📚 Learning Article: {os.path.basename(article_path)}")
        print("=" * 50)
        return True

    except Exception as e:
        print(f"❌ Error processing {video_filename}: {e}")
        print("⚠ Original video file preserved due to processing error.")
        print("=" * 50)
        return False

def main():
    print("Checking for new video and audio files...")
    for root, _, files in os.walk(INPUT_FOLDER):
        for filename in files:
            if filename.lower().endswith((".mp4", ".mp3")):
                file_path = os.path.join(root, filename)
                relative_path = os.path.relpath(root, INPUT_FOLDER)
                if relative_path == ".":
                    relative_path = ""
                process_video(file_path, relative_path)
    print("Finished checking for video and audio files.")

if __name__ == "__main__":
    main()

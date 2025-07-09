import os
import assemblyai as aai
from article_generator import ArticleGenerator
from dotenv import load_dotenv  # Add dotenv import

load_dotenv()  # Load environment variables

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
LEARNING_ARTICLES_FOLDER = os.path.join(SCRIPT_DIR, "LearningArticles")

# Ensure output folders exist
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(LEARNING_ARTICLES_FOLDER, exist_ok=True)

def process_video(video_path):
    video_filename = os.path.basename(video_path)
    base_name = os.path.splitext(video_filename)[0]
    
    mp3_path = os.path.join(OUTPUT_FOLDER, f"{base_name}.mp3")
    markdown_path = os.path.join(OUTPUT_FOLDER, f"{base_name}.md")
    article_path = os.path.join(LEARNING_ARTICLES_FOLDER, f"{base_name}_article.md")

    print(f"Processing: {video_filename}")
    print("=" * 50)

    try:
        # 1. Convert MP4 to MP3 using pydub (if available)
        print("Step 1: Audio extraction...")
        if PYDUB_AVAILABLE:
            audio = AudioSegment.from_file(video_path, format="mp4")
            audio.export(mp3_path, format="mp3")
            print(f"✓ Extracted audio to: {mp3_path}")
            audio_file_path = mp3_path
        else:
            print("⚠ pydub not available, attempting to transcribe video file directly...")
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
            transcript_text = transcript.text
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

        # 5. Clean up temporary MP3 (only if we created one)
        if PYDUB_AVAILABLE and os.path.exists(mp3_path):
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

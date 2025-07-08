#!/usr/bin/env python3
"""
Test script to generate a learning article from an existing transcript
"""

import os
from article_generator import ArticleGenerator

def test_article_generation():
    """Test the article generation with existing transcript"""
    
    # Set up paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    transcript_path = os.path.join(script_dir, "OutputMarkdown", "IT_Factor_1.2_Building_Charisma.md")
    output_dir = os.path.join(script_dir, "LearningArticles")
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    print("Testing Article Generation")
    print("=" * 50)
    
    # Check if transcript exists
    if not os.path.exists(transcript_path):
        print(f"❌ Transcript file not found: {transcript_path}")
        return False
    
    try:
        # Read the existing transcript
        with open(transcript_path, 'r', encoding='utf-8') as f:
            transcript_content = f.read()
        
        print(f"✓ Found transcript: {os.path.basename(transcript_path)}")
        print(f"✓ Transcript length: {len(transcript_content):,} characters")
        
        # Initialize article generator
        print("\nInitializing Gemini AI...")
        generator = ArticleGenerator()
        print("✓ Gemini AI initialized successfully")
        
        # Generate the learning article
        print("\nGenerating learning article...")
        video_filename = "IT_Factor_1.2_Building_Charisma.mp4"
        article_content, metadata = generator.generate_article(transcript_content, video_filename)
        
        # Save the article
        article_filename = "IT_Factor_1.2_Building_Charisma_article.md"
        article_path = os.path.join(output_dir, article_filename)
        generator.save_article(article_content, article_path, metadata)
        
        print(f"\n🎉 Success! Learning article generated:")
        print(f"📚 Article: {article_filename}")
        print(f"💰 Estimated cost: ${metadata['estimated_cost_usd']:.6f}")
        print(f"⏱️ Processing time: {metadata['processing_time_seconds']} seconds")
        print(f"📊 Tokens: {metadata['estimated_input_tokens']:,} input, {metadata['estimated_output_tokens']:,} output")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during article generation: {e}")
        return False

if __name__ == "__main__":
    # Check if API key is set
    if not os.environ.get("GEMINI_API_KEY"):
        print("❌ GEMINI_API_KEY environment variable not set.")
        print("Please set your Google Gemini API key:")
        print("  export GEMINI_API_KEY=\"your_gemini_api_key_here\"")
        exit(1)
    
    success = test_article_generation()
    if success:
        print("\n✅ Test completed successfully!")
    else:
        print("\n❌ Test failed!")

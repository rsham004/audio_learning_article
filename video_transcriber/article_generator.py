import os
import time
import logging
from typing import Optional, Tuple
import google.generativeai as genai
from dotenv import load_dotenv  # Add dotenv import

load_dotenv('.env')  # Specify .env file location

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ArticleGenerator:
    """
    Generates learning articles from transcripts using Google Gemini AI
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the ArticleGenerator with Gemini API key
        
        Args:
            api_key: Google Gemini API key. If None, will try to get from environment
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")  # Use getenv for consistency
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not provided and not found in environment variables")
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Cost tracking (approximate rates for Gemini 1.5 Flash)
        self.input_cost_per_1k_tokens = 0.000075  # $0.075 per 1M tokens
        self.output_cost_per_1k_tokens = 0.0003   # $0.30 per 1M tokens
        
    def create_learning_article_prompt(self, transcript: str, video_title: str) -> str:
        """
        Create a structured prompt for generating learning articles
        
        Args:
            transcript: The raw transcript text
            video_title: Title of the original video
            
        Returns:
            Formatted prompt for the LLM
        """
        prompt = f"""
You are an expert educational content creator. Transform the following transcript into a comprehensive, well-structured learning article.

**Original Video:** {video_title}

**Instructions:**
1. Create a professional learning article with clear sections
2. Elaborate on **all sections** in detail
3. Expand all concepts mentioned in the transcript with thorough explanations
4. Add context, examples, and applications for every topic
5. Structure the content logically for learning progression
6. Use markdown formatting with proper headings and subheadings
7. Ensure clarity and readability for educational purposes
8. Make the content engaging and practical

**Required Article Structure:**
# [Descriptive Title Based on Content]

## Executive Summary
Brief overview of what this article covers and key insights

## Learning Objectives
What readers will learn from this article (3-5 bullet points)

## Introduction
Context and background for the topic

## Core Concepts
### [Concept 1]
Detailed explanation with examples

### [Concept 2] 
Detailed explanation with examples

[Continue for all major concepts]

## Detailed Analysis
Deep dive into the most important topics with:
- Explanations of techniques or methods
- Real-world applications
- Examples and scenarios

## Practical Applications
How to apply these concepts in real situations

## Key Takeaways
- Summarize the most important points (5-7 bullet points)
- Focus on actionable insights

## Conclusion
Wrap up the main themes and encourage further learning

---

**Transcript to Transform:**

{transcript}

**Generate the learning article now:**
"""
        return prompt
    
    def estimate_tokens(self, text: str) -> int:
        """
        Estimate token count for cost calculation
        Rough approximation: 1 token ≈ 4 characters
        """
        return len(text) // 4
    
    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """
        Calculate estimated cost for the API call
        
        Args:
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            
        Returns:
            Estimated cost in USD
        """
        input_cost = (input_tokens / 1000) * self.input_cost_per_1k_tokens
        output_cost = (output_tokens / 1000) * self.output_cost_per_1k_tokens
        return input_cost + output_cost
    
    def generate_article(self, transcript: str, video_filename: str) -> Tuple[str, dict]:
        """
        Generate a learning article from a transcript
        
        Args:
            transcript: The raw transcript text
            video_filename: Original video filename for context
            
        Returns:
            Tuple of (generated_article, metadata)
        """
        start_time = time.time()
        
        # Clean up video filename for title
        video_title = os.path.splitext(video_filename)[0].replace('_', ' ').replace('-', ' ')
        
        # Create prompt
        prompt = self.create_learning_article_prompt(transcript, video_title)
        
        # Estimate input tokens
        input_tokens = self.estimate_tokens(prompt)
        
        logger.info(f"Generating learning article for: {video_filename}")
        logger.info(f"Estimated input tokens: {input_tokens:,}")
        
        try:
            # Generate content with Gemini
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    top_p=0.8,
                    top_k=40,
                    max_output_tokens=4000,
                )
            )
            
            # Extract generated text
            if response.text:
                generated_article = response.text.strip()
                
                # Estimate output tokens and cost
                output_tokens = self.estimate_tokens(generated_article)
                estimated_cost = self.calculate_cost(input_tokens, output_tokens)
                
                processing_time = time.time() - start_time
                
                # Create metadata
                metadata = {
                    'video_filename': video_filename,
                    'processing_time_seconds': round(processing_time, 2),
                    'estimated_input_tokens': input_tokens,
                    'estimated_output_tokens': output_tokens,
                    'estimated_cost_usd': round(estimated_cost, 6),
                    'model_used': 'gemini-1.5-flash',
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                }
                
                logger.info(f"Article generated successfully!")
                logger.info(f"Processing time: {processing_time:.2f} seconds")
                logger.info(f"Estimated cost: ${estimated_cost:.6f}")
                logger.info(f"Output tokens: {output_tokens:,}")
                
                return generated_article, metadata
            else:
                raise Exception("No content generated by Gemini")
                
        except Exception as e:
            logger.error(f"Error generating article: {str(e)}")
            raise
    
    def save_article(self, article_content: str, output_path: str, metadata: dict) -> None:
        """
        Save the generated article to a file with metadata
        
        Args:
            article_content: The generated article text
            output_path: Path where to save the article
            metadata: Processing metadata to include
        """
        try:
            # Add metadata footer to the article
            article_with_metadata = f"""{article_content}

---

**Article Generation Metadata:**
- Original Video: {metadata['video_filename']}
- Generated: {metadata['timestamp']}
- Processing Time: {metadata['processing_time_seconds']} seconds
- Model: {metadata['model_used']}
- Estimated Cost: ${metadata['estimated_cost_usd']:.6f}
- Tokens: {metadata['estimated_input_tokens']:,} input, {metadata['estimated_output_tokens']:,} output
"""
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(article_with_metadata)
            
            logger.info(f"Article saved to: {output_path}")
            
        except Exception as e:
            logger.error(f"Error saving article: {str(e)}")
            raise

def main():
    """
    Test function for the ArticleGenerator
    """
    # This is for testing purposes
    generator = ArticleGenerator()
    
    # Test with a sample transcript
    sample_transcript = "This is a test transcript about learning and development."
    article, metadata = generator.generate_article(sample_transcript, "test_video.mp4")
    
    print("Generated Article:")
    print(article)
    print("\nMetadata:")
    print(metadata)

if __name__ == "__main__":
    main()

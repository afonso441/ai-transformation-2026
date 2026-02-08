"""
Day 2: Production-ready error handling for Claude API
Goal: Build reliable code that handles failures gracefully
"""

import anthropic
import os
import time
from dotenv import load_dotenv

load_dotenv()

def ask_claude_with_retry(question, max_retries=3):
    """
    Ask Claude a question with automatic retry on failure
    
    This pattern is essential for production applications.
    Similar to retry logic in embedded systems communication.
    """
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    for attempt in range(max_retries):
        try:
            print(f"Attempt {attempt + 1}/{max_retries}...")
            
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=500,
                messages=[{"role": "user", "content": question}]
            )
            
            print("✅ Success!")
            return response.content[0].text
            
        except anthropic.APIError as e:
            print(f"❌ API Error: {e}")
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
                print(f"⏳ Waiting {wait_time}s before retry...")
                time.sleep(wait_time)
            else:
                print("❌ Max retries reached. Giving up.")
                raise
                
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            raise

# Test it
if __name__ == "__main__":
    print("="*60)
    print("Testing error handling with retries")
    print("="*60)
    
    question = "Explain error handling in Python in 2 sentences."
    answer = ask_claude_with_retry(question)
    
    print("\n" + "="*60)
    print("ANSWER:")
    print("="*60)
    print(answer)
    print("="*60)
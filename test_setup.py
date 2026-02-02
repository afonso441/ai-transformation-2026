import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check if API key loaded
api_key = os.getenv("ANTHROPIC_API_KEY")

if api_key:
    # Don't print the full key for security!
    print("✅ API key loaded successfully!")
    print(f"   Key starts with: {api_key[:15]}...")
else:
    print("❌ API key not found. Check your .env file.")
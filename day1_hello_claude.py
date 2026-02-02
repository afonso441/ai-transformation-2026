"""
Day 1: First Claude API Call
Goal: Successfully communicate with Claude
"""

import anthropic
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment
api_key = os.getenv("ANTHROPIC_API_KEY")

# Initialize the client
client = anthropic.Anthropic(api_key=api_key)

# Make your first API call
print("🚀 Making first API call to Claude...")

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Hello Claude! I'm an embedded systems engineer with 20 years of C/C++ experience. Today is Day 1 of my 14-month transformation into an AI engineer. Give me one powerful piece of advice to start strong."
        }
    ]
)

# Print the response
print("\n" + "="*50)
print("CLAUDE'S RESPONSE:")
print("="*50)
print(message.content[0].text)
print("="*50)

print("\n✅ Success! Your first AI API call works!")
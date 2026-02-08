"""
Day 3: Understanding System Prompts
Goal: See the difference system prompts make
"""

import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def ask_without_system_prompt(question):
    """No system prompt - default Claude behavior"""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        messages=[{"role": "user", "content": question}]
    )
    return response.content[0].text

def ask_with_system_prompt(question, system_prompt):
    """With system prompt - customized behavior"""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        system=system_prompt,  # ← The key difference!
        messages=[{"role": "user", "content": question}]
    )
    return response.content[0].text

# Test question
question = "Explain how interrupts work in embedded systems."

print("="*60)
print("EXPERIMENT: System Prompt Impact")
print("="*60)

# Without system prompt
print("\n1️⃣  WITHOUT SYSTEM PROMPT:")
print("-"*60)
answer1 = ask_without_system_prompt(question)
print(answer1)

# With embedded expert system prompt
system_prompt = """You are an embedded systems expert with 20+ years of experience.
When explaining concepts:
- Use analogies from hardware and C programming
- Be concise and practical
- Focus on real-world implementation details
- Mention common pitfalls
- Reference specific hardware (ARM Cortex-M, AVR, etc.)"""

print("\n2️⃣  WITH EMBEDDED EXPERT SYSTEM PROMPT:")
print("-"*60)
answer2 = ask_with_system_prompt(question, system_prompt)
print(answer2)

print("\n" + "="*60)
print("✅ Notice the difference?")
print("System prompts customize AI behavior!")
print("="*60)
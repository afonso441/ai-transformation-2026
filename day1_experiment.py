"""
Day 1 Experiments: Try different prompts
"""

import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def ask_claude(question):
    """Helper function to ask Claude anything"""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,  # Shorter responses for experiments
        messages=[{"role": "user", "content": question}]
    )
    return response.content[0].text

# Experiment 1: Technical explanation
print("EXPERIMENT 1: Technical Explanation")
print("="*50)
answer = ask_claude(
    "Explain what an API is, but use analogies from embedded systems and hardware engineering."
)
print(answer)
print("\n")

# Experiment 2: Code generation
print("EXPERIMENT 2: Code Generation")
print("="*50)
answer = ask_claude(
    "Write a Python function that converts Celsius to Fahrenheit. Include docstring and type hints."
)
print(answer)
print("\n")

# Experiment 3: Compare to C
print("EXPERIMENT 3: C to Python Translation")
print("="*50)
answer = ask_claude(
    """I'm a C programmer learning Python. Explain the key differences between:
    
    C:
    int* ptr = malloc(sizeof(int) * 10);
    free(ptr);
    
    Python:
    my_list = [0] * 10
    """
)
print(answer)
"""
Day 2: Experimenting with different prompt styles
Goal: Learn what makes a good prompt vs bad prompt
"""

import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def ask_claude(prompt, description=""):
    """Helper function to ask Claude and display results"""
    if description:
        print(f"\n{'='*60}")
        print(f"EXPERIMENT: {description}")
        print(f"{'='*60}")
        print(f"PROMPT:\n{prompt}\n")
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}]
    )
    
    answer = response.content[0].text
    print(f"RESPONSE:\n{answer}\n")
    return answer

# Experiment 1: Vague vs Specific
print("\n🔬 PROMPT ENGINEERING EXPERIMENTS\n")

ask_claude(
    "Tell me about pointers",
    "1. VAGUE PROMPT (Bad)"
)

ask_claude(
    "Explain C pointers to someone with embedded systems experience. Focus on: 1) Memory addressing, 2) Pointer arithmetic, 3) Common pitfalls. Use 3-4 sentences.",
    "2. SPECIFIC PROMPT (Good)"
)

# Experiment 2: Context matters
ask_claude(
    "What's the difference between malloc and stack allocation?",
    "3. NO CONTEXT"
)

ask_claude(
    "I'm an embedded C programmer learning Python. Explain how Python's memory management differs from C's malloc/free pattern. Use analogies from embedded systems.",
    "4. WITH CONTEXT (Better)"
)

# Experiment 3: Output format specification
ask_claude(
    "Compare Python and C",
    "5. NO FORMAT SPECIFIED"
)

ask_claude(
    """Compare Python and C for these features:
- Memory management
- Execution speed  
- Development speed
- Use cases

Format as a simple comparison list.""",
    "6. FORMAT SPECIFIED (Structured)"
)

print("\n" + "="*60)
print("✅ Experiments complete!")
print("\n💡 KEY LEARNING:")
print("Specific prompts with context + format = 10x better results")
print("="*60)
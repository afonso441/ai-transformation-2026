"""
Week 3 Day 1: Role-Based System Prompts
Goal: See how different roles change AI behavior
"""

import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def ask_with_role(question, role_prompt, role_name):
    """Ask the same question with different role prompts"""
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        system=role_prompt,
        messages=[{"role": "user", "content": question}]
    )
    
    return response.content[0].text

# ============================================================================
# DIFFERENT ROLES FOR THE SAME QUESTION
# ============================================================================

question = "Explain how interrupts work in microcontrollers."

roles = {
    "Beginner Teacher": """You are a patient teacher explaining to someone 
who just started learning embedded systems. Use simple language, analogies, 
and avoid jargon. Be encouraging and clear.""",
    
    "Senior Engineer": """You are a senior embedded systems engineer with 
20+ years experience. Be technical, precise, and mention edge cases. Assume 
the reader is experienced. Focus on practical implementation details.""",
    
    "Technical Writer": """You are a technical documentation writer. Create 
clear, well-structured explanations with:
- Brief overview
- Step-by-step explanation
- Code example
- Common pitfalls
Use professional but accessible language.""",
    
    "University Professor": """You are a computer engineering professor 
teaching interrupt handling. Provide:
- Theoretical foundation
- Hardware mechanism
- Software perspective
- Real-world applications
Be rigorous and academic.""",
    
    "Code Reviewer": """You are reviewing interrupt handling code. Focus on:
- Correct implementation patterns
- Common mistakes to avoid
- Performance considerations
- Best practices
Be critical but constructive."""
}

# ============================================================================
# TEST EACH ROLE
# ============================================================================

print("\n" + "="*70)
print("ROLE-BASED SYSTEM PROMPTS COMPARISON")
print("="*70)
print(f"\nQuestion: {question}\n")

for role_name, role_prompt in roles.items():
    print("="*70)
    print(f"🎭 ROLE: {role_name}")
    print("="*70)
    print()
    
    answer = ask_with_role(question, role_prompt, role_name)
    print(answer)
    print()
    
    input("⏎ Press Enter for next role...\n")

print("="*70)
print("✅ Role comparison complete!")
print("\n💡 KEY INSIGHT: Same question, different roles = different answers")
print("   Choose the right role for your use case!")
print("="*70)
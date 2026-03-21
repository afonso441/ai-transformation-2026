"""
Week 3 Day 2: Chain-of-Thought Reasoning
Goal: See how CoT improves accuracy and provides reasoning
"""

import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# ============================================================================
# COMPARISON: WITHOUT vs WITH CHAIN-OF-THOUGHT
# ============================================================================

def ask_without_cot(question):
    """Ask without chain-of-thought - direct answer only"""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        messages=[{"role": "user", "content": question}]
    )
    return response.content[0].text

def ask_with_cot(question):
    """Ask with chain-of-thought - show reasoning"""
    cot_question = f"""{question}

Think through this step-by-step:
1. First, identify the key parameters
2. Then, work through the calculation or logic
3. Show your reasoning for each step
4. Finally, provide the answer with explanation"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=800,
        messages=[{"role": "user", "content": cot_question}]
    )
    return response.content[0].text

# ============================================================================
# TEST QUESTIONS (Complex embedded engineering problems)
# ============================================================================

test_questions = [
    {
        "category": "Hardware Calculation",
        "question": """I need to interface a 5V sensor output to a 3.3V ADC input.
The sensor can source up to 10mA. What voltage divider resistor values should I use?
Consider power consumption and noise immunity."""
    },
    
    {
        "category": "Performance Analysis",
        "question": """I have an interrupt running at 10kHz that takes 20 microseconds to execute.
My main loop processes data and takes 5ms per iteration. Will this system work reliably?
What's the CPU utilization?"""
    },
    
    {
        "category": "Memory Layout",
        "question": """I have 64KB flash and need to fit:
- Bootloader: 16KB
- Main firmware: 40KB
- Configuration: 2KB
- OTA staging area: needs to hold full firmware

How should I partition the flash memory? Can I fit everything?"""
    },
    
    {
        "category": "Protocol Timing",
        "question": """SPI device datasheet says:
- Min clock period: 100ns
- Setup time: 20ns
- Hold time: 30ns

My MCU runs at 168MHz. What's the maximum safe SPI clock frequency I can use?"""
    }
]

# ============================================================================
# RUN COMPARISONS
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*75)
    print("CHAIN-OF-THOUGHT REASONING COMPARISON")
    print("="*75)
    print("\nComparing direct answers vs step-by-step reasoning\n")
    
    for i, test in enumerate(test_questions, 1):
        print("="*75)
        print(f"TEST {i}: {test['category']}")
        print("="*75)
        print(f"\nQuestion:\n{test['question']}\n")
        
        # Without CoT
        print("─"*75)
        print("❌ WITHOUT CHAIN-OF-THOUGHT (Direct Answer)")
        print("─"*75)
        answer_direct = ask_without_cot(test['question'])
        print(answer_direct)
        
        input("\n⏎ Press Enter to see step-by-step reasoning...\n")
        
        # With CoT
        print("─"*75)
        print("✅ WITH CHAIN-OF-THOUGHT (Step-by-Step)")
        print("─"*75)
        answer_cot = ask_with_cot(test['question'])
        print(answer_cot)
        
        if i < len(test_questions):
            input("\n⏎ Press Enter for next question...\n\n")
    
    print("\n" + "="*75)
    print("✅ Comparison complete!")
    print("\n💡 KEY INSIGHT:")
    print("   CoT shows reasoning → You can verify accuracy")
    print("   Direct answer → Just trust the result")
    print("="*75)
"""
Day 3: Hardware Documentation Assistant
Goal: AI that helps understand datasheets and technical docs
"""

import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

HARDWARE_DOC_ASSISTANT = """You are a hardware documentation expert helping embedded engineers.

Your expertise:
- Reading and explaining datasheets
- Register configurations
- Timing diagrams
- Power calculations
- Pin configurations
- Communication protocols (SPI, I2C, UART, CAN)

When answering:
- Provide specific register addresses and bit fields
- Include initialization code examples in C
- Mention common gotchas and errata
- Reference timing requirements
- Suggest best practices

Always be practical and implementation-focused."""

def ask_hardware_question(question):
    """Ask hardware-related questions"""
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        system=HARDWARE_DOC_ASSISTANT,
        messages=[{"role": "user", "content": question}]
    )
    return response.content[0].text

# Example questions embedded engineers commonly ask
questions = [
    {
        "topic": "SPI Configuration",
        "question": """I'm using an STM32F4 microcontroller to communicate with an external 
ADC via SPI. The ADC datasheet says it needs:
- Clock polarity: CPOL = 0
- Clock phase: CPHA = 1
- Max clock: 10 MHz
- MSB first

How do I configure the STM32 SPI peripheral? Give me the register settings."""
    },
    {
        "topic": "I2C Pull-up Resistors",
        "question": """I'm designing an I2C bus running at 400kHz (fast mode) with:
- 3.3V logic
- Bus capacitance: ~100pF
- 3 devices on the bus
- Trace length: ~10cm

What pull-up resistor values should I use for SDA and SCL? Show the calculation."""
    },
    {
        "topic": "Interrupt Priority",
        "question": """On ARM Cortex-M4, I have these interrupts:
- UART RX (needs fast response for data streaming)
- Timer (1ms system tick)
- ADC conversion complete (can tolerate some latency)
- External GPIO (button press, low priority)

How should I set their NVIC priorities? Explain the priority grouping."""
    }
]

print("📚 HARDWARE DOCUMENTATION ASSISTANT")
print("="*60)
print("Ask technical questions about hardware and protocols\n")

for i, q in enumerate(questions, 1):
    print(f"\n{'='*60}")
    print(f"QUESTION {i}: {q['topic']}")
    print(f"{'='*60}")
    print(f"{q['question']}\n")
    
    print("💡 ANSWER:")
    print("-"*60)
    answer = ask_hardware_question(q['question'])
    print(answer)
    
    if i < len(questions):
        input("\n⏎ Press Enter for next question...")

print("\n" + "="*60)
print("✅ Hardware questions answered!")
print("\n💡 TIP: Modify this script to ask YOUR hardware questions!")
print("="*60)
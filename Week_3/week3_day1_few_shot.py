"""
Week 3 Day 1: Few-Shot Learning
Goal: Teach AI by examples (like calibration in embedded systems)
"""

import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# ============================================================================
# EXAMPLE 1: CODE DOCUMENTATION STYLE
# ============================================================================

def generate_documentation_few_shot():
    """Use few-shot learning to generate consistent documentation"""
    
    # Define the style with examples
    system_prompt = """You are a code documentation expert. Follow this exact style:

Example 1:
Input: void init_uart(uint32_t baudrate) { UART_BRR = baudrate; }
Output:
/**
 * Initialize UART peripheral
 * @param baudrate Communication speed in bps
 * @complexity O(1)
 * @side_effects Modifies UART_BRR register
 */

Example 2:
Input: int read_sensor(void) { return ADC_DATA; }
Output:
/**
 * Read current sensor value
 * @return Raw ADC reading (0-4095)
 * @complexity O(1)
 * @side_effects None - read-only operation
 */

Now generate documentation in this exact style."""

    # New code to document
    new_code = "void set_pwm(uint8_t channel, uint16_t duty_cycle) { PWM_REG[channel] = duty_cycle; }"
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        system=system_prompt,
        messages=[{
            "role": "user",
            "content": f"Generate documentation for:\n{new_code}"
        }]
    )
    
    return response.content[0].text

# ============================================================================
# EXAMPLE 2: ERROR MESSAGE FORMATTING
# ============================================================================

def generate_error_messages_few_shot():
    """Teach AI to format error messages consistently"""
    
    system_prompt = """You format embedded system error messages. Follow these examples:

Example 1:
Input: UART buffer overflow
Output:
[ERROR] UART_RX_OVERFLOW
Cause: Receive buffer full (256 bytes)
Action: Increase buffer size or reduce baud rate
Code: 0x0101

Example 2:
Input: SPI timeout
Output:
[ERROR] SPI_TIMEOUT
Cause: No response from peripheral after 1000ms
Action: Check SPI clock, verify peripheral power
Code: 0x0201

Use this exact format for all errors."""

    new_error = "I2C address not acknowledged"
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        system=system_prompt,
        messages=[{
            "role": "user",
            "content": f"Format this error:\n{new_error}"
        }]
    )
    
    return response.content[0].text

# ============================================================================
# EXAMPLE 3: REGISTER CONFIGURATION PARSER
# ============================================================================

def parse_register_config_few_shot():
    """Teach AI to parse register configs in specific format"""
    
    system_prompt = """You parse register configurations. Follow these examples:

Example 1:
Input: "Set UART CR1 register: enable UART, 8-bit data, no parity"
Output:
```c
UART->CR1 = 0;           // Clear register
UART->CR1 |= (1 << 13);  // UE: UART enable
UART->CR1 |= (0 << 12);  // M: 8-bit data
UART->CR1 |= (0 << 10);  // PCE: Parity disabled
```

Example 2:
Input: "Configure SPI CR1: master mode, 8MHz clock, CPOL=0, CPHA=1"
Output:
```c
SPI->CR1 = 0;            // Clear register
SPI->CR1 |= (1 << 2);    // MSTR: Master mode
SPI->CR1 |= (0b010 << 3);// BR: fPCLK/8 = 8MHz
SPI->CR1 |= (0 << 1);    // CPOL: Clock polarity 0
SPI->CR1 |= (1 << 0);    // CPHA: Clock phase 1
```

Generate code in this style."""

    new_config = "Setup ADC CR2: enable ADC, continuous conversion, external trigger"
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=400,
        system=system_prompt,
        messages=[{
            "role": "user",
            "content": f"Generate configuration code:\n{new_config}"
        }]
    )
    
    return response.content[0].text

# ============================================================================
# TEST ALL EXAMPLES
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("FEW-SHOT LEARNING EXAMPLES")
    print("="*70)
    
    # Example 1: Code documentation
    print("\n📝 EXAMPLE 1: Code Documentation Style")
    print("-"*70)
    doc = generate_documentation_few_shot()
    print(doc)
    
    input("\n⏎ Press Enter for next example...\n")
    
    # Example 2: Error messages
    print("\n⚠️  EXAMPLE 2: Error Message Formatting")
    print("-"*70)
    error_msg = generate_error_messages_few_shot()
    print(error_msg)
    
    input("\n⏎ Press Enter for next example...\n")
    
    # Example 3: Register config
    print("\n⚙️  EXAMPLE 3: Register Configuration Code")
    print("-"*70)
    register_code = parse_register_config_few_shot()
    print(register_code)
    
    print("\n" + "="*70)
    print("✅ Few-shot learning examples complete!")
    print("\n💡 KEY INSIGHT: Show AI 2-3 examples = consistent output format")
    print("   Like calibrating sensors with known inputs!")
    print("="*70)
"""
Week 3 Day 1: Automatic Code Documenter
Goal: Practical tool using advanced prompting techniques
"""

import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# ============================================================================
# CODE DOCUMENTER WITH FEW-SHOT LEARNING
# ============================================================================

DOCUMENTATION_SYSTEM_PROMPT = """You are an embedded C code documentation expert.

Generate Doxygen-style documentation following this format:

Example Input:
```c
void init_timer(uint32_t period_ms) {
    TIM->PSC = (SystemCoreClock / 1000) - 1;
    TIM->ARR = period_ms - 1;
    TIM->CR1 |= TIM_CR1_CEN;
}
```

Example Output:
```c
/**
 * @brief Initialize hardware timer with specified period
 * @param period_ms Timer period in milliseconds (1-65535)
 * @note Assumes SystemCoreClock is configured
 * @warning Modifies TIM peripheral registers directly
 * @complexity O(1) - Direct register access
 * 
 * @details
 * Configures timer prescaler for 1kHz tick rate, sets auto-reload
 * register for desired period, and enables the timer.
 * 
 * @example
 * init_timer(1000);  // 1 second timer period
 */
void init_timer(uint32_t period_ms) {
    TIM->PSC = (SystemCoreClock / 1000) - 1;  // 1ms tick
    TIM->ARR = period_ms - 1;                  // Period
    TIM->CR1 |= TIM_CR1_CEN;                   // Enable timer
}
```

Generate documentation in this exact style for any C function provided."""

def document_code(code):
    """Generate documentation for C code"""
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=800,
        system=DOCUMENTATION_SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": f"Document this function:\n\n```c\n{code}\n```"
        }]
    )
    
    return response.content[0].text

# ============================================================================
# TEST WITH REAL EMBEDDED CODE
# ============================================================================

test_functions = [
    """
void read_adc(uint8_t channel) {
    ADC->SQR1 = (channel & 0x1F);
    ADC->CR2 |= ADC_CR2_SWSTART;
    while(!(ADC->SR & ADC_SR_EOC));
    return ADC->DR;
}
    """,
    
    """
void send_uart(const char* str) {
    while(*str) {
        while(!(UART->SR & UART_SR_TXE));
        UART->DR = *str++;
    }
}
    """,
    
    """
void configure_gpio(GPIO_TypeDef* port, uint8_t pin, uint8_t mode) {
    uint32_t pos = pin * 2;
    port->MODER &= ~(0x3 << pos);
    port->MODER |= (mode << pos);
}
    """
]

if __name__ == "__main__":
    print("\n" + "="*70)
    print("AUTOMATIC CODE DOCUMENTER")
    print("="*70)
    print("Generates professional Doxygen documentation for C functions\n")
    
    for i, code in enumerate(test_functions, 1):
        print("="*70)
        print(f"FUNCTION {i}")
        print("="*70)
        print("\nOriginal code:")
        print(code.strip())
        
        print("\n⏳ Generating documentation...")
        documented = document_code(code.strip())
        
        print("\n📝 Generated documentation:")
        print("-"*70)
        print(documented)
        
        if i < len(test_functions):
            input("\n⏎ Press Enter for next function...\n")
    
    print("\n" + "="*70)
    print("✅ Code documentation complete!")
    print("\n💡 TIP: Use this on YOUR actual embedded code!")
    print("   Just paste your functions into the test_functions list.")
    print("="*70)
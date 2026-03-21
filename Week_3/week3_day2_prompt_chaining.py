"""
Week 3 Day 2: Prompt Chaining
Goal: Break complex tasks into sequential steps
"""

import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# ============================================================================
# EXAMPLE: MULTI-STEP CODE REVIEW PROCESS
# ============================================================================

def step1_extract_functions(code):
    """Step 1: Extract all functions from code"""
    prompt = f"""Analyze this C code and extract all function definitions.

Code:
```c
{code}
```

For each function, provide:
- Function name
- Parameters
- Return type
- Brief description of what it does

Format as a numbered list."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=800,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.content[0].text

def step2_analyze_complexity(function_list, code):
    """Step 2: Analyze complexity of each function"""
    prompt = f"""Given these functions from embedded C code:

{function_list}

Original code:
```c
{code}
```

For each function, analyze:
- Time complexity (Big O)
- Space complexity
- Number of nested loops
- Recursion depth (if any)

Identify which functions are performance-critical."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.content[0].text

def step3_find_bottlenecks(complexity_analysis, code):
    """Step 3: Identify performance bottlenecks"""
    prompt = f"""Based on this complexity analysis:

{complexity_analysis}

Original code:
```c
{code}
```

Identify:
1. Performance bottlenecks (functions called frequently + high complexity)
2. Memory inefficiencies (unnecessary allocations, large stack usage)
3. Cache-unfriendly patterns (random access, non-contiguous memory)

Prioritize issues by impact."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.content[0].text

def step4_suggest_optimizations(bottlenecks, code):
    """Step 4: Suggest specific optimizations"""
    prompt = f"""Given these bottlenecks:

{bottlenecks}

Original code:
```c
{code}
```

Provide specific optimization recommendations:
1. Code changes (with before/after examples)
2. Expected performance improvement
3. Trade-offs (readability, memory, etc.)

Focus on highest-impact optimizations first."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1200,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.content[0].text

# ============================================================================
# COMPLETE CHAINED WORKFLOW
# ============================================================================

def analyze_code_performance(code):
    """
    Complete multi-step code analysis using prompt chaining
    
    Pipeline:
    Code → Extract functions → Analyze complexity → 
    Find bottlenecks → Suggest optimizations
    """
    
    print("\n" + "="*75)
    print("MULTI-STEP CODE PERFORMANCE ANALYSIS")
    print("="*75)
    
    # Step 1: Extract functions
    print("\n📋 STEP 1: Extracting functions...")
    print("─"*75)
    functions = step1_extract_functions(code)
    print(functions)
    
    input("\n⏎ Press Enter to continue to complexity analysis...\n")
    
    # Step 2: Analyze complexity
    print("\n📊 STEP 2: Analyzing complexity...")
    print("─"*75)
    complexity = step2_analyze_complexity(functions, code)
    print(complexity)
    
    input("\n⏎ Press Enter to identify bottlenecks...\n")
    
    # Step 3: Find bottlenecks
    print("\n⚠️  STEP 3: Identifying bottlenecks...")
    print("─"*75)
    bottlenecks = step3_find_bottlenecks(complexity, code)
    print(bottlenecks)
    
    input("\n⏎ Press Enter for optimization suggestions...\n")
    
    # Step 4: Suggest optimizations
    print("\n💡 STEP 4: Optimization recommendations...")
    print("─"*75)
    optimizations = step4_suggest_optimizations(bottlenecks, code)
    print(optimizations)
    
    print("\n" + "="*75)
    print("✅ Complete analysis finished!")
    print("="*75)
    
    return {
        "functions": functions,
        "complexity": complexity,
        "bottlenecks": bottlenecks,
        "optimizations": optimizations
    }

# ============================================================================
# TEST CODE (Performance-critical embedded function)
# ============================================================================

test_code = """
// Sensor data processing - called 1000 times per second
void process_sensor_data(int16_t *samples, int count) {
    // Moving average filter
    for (int i = 0; i < count; i++) {
        int32_t sum = 0;
        for (int j = -5; j <= 5; j++) {
            int idx = i + j;
            if (idx >= 0 && idx < count) {
                sum += samples[idx];
            }
        }
        samples[i] = sum / 11;
    }
    
    // Find peaks
    for (int i = 1; i < count - 1; i++) {
        if (samples[i] > samples[i-1] && samples[i] > samples[i+1]) {
            mark_peak(i, samples[i]);
        }
    }
    
    // Calculate statistics
    int32_t mean = 0;
    for (int i = 0; i < count; i++) {
        mean += samples[i];
    }
    mean /= count;
    
    int32_t variance = 0;
    for (int i = 0; i < count; i++) {
        int32_t diff = samples[i] - mean;
        variance += diff * diff;
    }
    variance /= count;
}

void mark_peak(int index, int16_t value) {
    // Record peak location and value
    if (peak_count < MAX_PEAKS) {
        peaks[peak_count].index = index;
        peaks[peak_count].value = value;
        peak_count++;
    }
}
"""

# ============================================================================
# RUN ANALYSIS
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*75)
    print("PROMPT CHAINING DEMONSTRATION")
    print("="*75)
    print("\nAnalyzing embedded code through 4-step pipeline:")
    print("1. Extract functions")
    print("2. Analyze complexity")
    print("3. Find bottlenecks")
    print("4. Suggest optimizations")
    print()
    
    result = analyze_code_performance(test_code)
    
    print("\n💡 KEY INSIGHT:")
    print("   Breaking complex task into steps = Better, more focused analysis")
    print("   Each step builds on previous results")
    print("="*75)
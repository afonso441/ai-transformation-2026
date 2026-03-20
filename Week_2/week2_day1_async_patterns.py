"""
Week 2 Day 1: Common Async Patterns
Goal: Learn practical async techniques
"""

import anthropic
import asyncio
import time
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# ============================================================================
# PATTERN 1: Simple Async Function
# ============================================================================

async def simple_async_call(question):
    """Basic async API call"""
    response = await client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=200,
        messages=[{"role": "user", "content": question}]
    )
    return response.content[0].text

# ============================================================================
# PATTERN 2: Error Handling in Async
# ============================================================================

async def async_with_error_handling(question):
    """Async call with try/except"""
    try:
        response = await client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=200,
            messages=[{"role": "user", "content": question}]
        )
        return response.content[0].text
    except anthropic.APIError as e:
        return f"API Error: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"

# ============================================================================
# PATTERN 3: Async with Timeout
# ============================================================================

async def async_with_timeout(question, timeout_seconds=5):
    """Async call with timeout protection"""
    try:
        response = await asyncio.wait_for(
            client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=200,
                messages=[{"role": "user", "content": question}]
            ),
            timeout=timeout_seconds
        )
        return response.content[0].text
    except asyncio.TimeoutError:
        return f"Request timed out after {timeout_seconds} seconds"

# ============================================================================
# PATTERN 4: Process Results as They Complete
# ============================================================================

async def process_as_completed():
    """Process async results as they finish (not in order)"""
    questions = [
        ("Short", "What is AI?"),
        ("Medium", "Explain machine learning in 2 sentences."),
        ("Long", "Describe the history of artificial intelligence in detail.")
    ]
    
    print("\n🔄 PATTERN: Process as completed (fastest first)")
    print("="*60)
    
    # Create tasks
    tasks = [
        asyncio.create_task(simple_async_call(q[1]), name=q[0])
        for q in questions
    ]
    
    # Process as they complete
    for coro in asyncio.as_completed(tasks):
        result = await coro
        # Get the task that just completed
        for task in tasks:
            if task.done() and task.result() == result:
                print(f"✓ {task.get_name()}: {len(result)} chars")
                break

# ============================================================================
# PATTERN 5: Batching with Delays
# ============================================================================

async def batched_requests():
    """Make requests in batches to avoid rate limits"""
    questions = [f"What is concept number {i}?" for i in range(10)]
    
    print("\n📦 PATTERN: Batched requests (groups of 3)")
    print("="*60)
    
    batch_size = 3
    all_results = []
    
    for i in range(0, len(questions), batch_size):
        batch = questions[i:i + batch_size]
        print(f"  Batch {i//batch_size + 1}: Processing {len(batch)} requests...")
        
        results = await asyncio.gather(*[
            simple_async_call(q) for q in batch
        ])
        
        all_results.extend(results)
        
        # Small delay between batches
        if i + batch_size < len(questions):
            await asyncio.sleep(0.5)
    
    print(f"✓ All {len(all_results)} requests complete!")
    return all_results

# ============================================================================
# MAIN: Run all patterns
# ============================================================================

async def main():
    print("\n" + "="*60)
    print("ASYNC PATTERNS DEMO")
    print("="*60)
    
    # Pattern 1: Simple
    print("\n✅ PATTERN 1: Simple async call")
    result = await simple_async_call("What is Python?")
    print(f"Result: {result[:80]}...")
    
    # Pattern 2: Error handling
    print("\n✅ PATTERN 2: With error handling")
    result = await async_with_error_handling("Explain async.")
    print(f"Result: {result[:80]}...")
    
    # Pattern 3: Timeout
    print("\n✅ PATTERN 3: With timeout")
    result = await async_with_timeout("What is programming?", timeout_seconds=10)
    print(f"Result: {result[:80]}...")
    
    # Pattern 4: As completed
    print("\n✅ PATTERN 4: Process as completed")
    await process_as_completed()
    
    # Pattern 5: Batched
    print("\n✅ PATTERN 5: Batched requests")
    await batched_requests()
    
    print("\n" + "="*60)
    print("✅ All patterns demonstrated!")
    print("="*60)

if __name__ == "__main__":
    asyncio.run(main())
"""
Week 2 Day 1: Sync vs Async Performance Comparison
Goal: See the dramatic speed difference async provides
"""

import anthropic
import asyncio
import time
import os
import sys
from dotenv import load_dotenv

load_dotenv()

# ============================================================================
# FIX FOR WINDOWS: Set event loop policy
# ============================================================================
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# ============================================================================
# SYNCHRONOUS APPROACH (Old Way - Slow)
# ============================================================================

def ask_claude_sync(question):
    """Make a synchronous Claude API call (blocking)"""
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        messages=[{"role": "user", "content": question}]
    )
    return response.content[0].text

def sync_example():
    """Ask 5 questions synchronously (one at a time)"""
    questions = [
        "What is async programming in one sentence?",
        "What is a REST API in one sentence?",
        "What is JSON in one sentence?",
        "What is HTTP in one sentence?",
        "What is an API endpoint in one sentence?"
    ]
    
    print("🐌 SYNCHRONOUS APPROACH (One at a time)")
    print("="*60)
    
    start_time = time.time()
    answers = []
    
    for i, question in enumerate(questions, 1):
        print(f"  {i}. Asking: {question[:40]}...")
        answer = ask_claude_sync(question)
        answers.append(answer)
        print(f"     ✓ Got answer ({len(answer)} chars)")
    
    elapsed = time.time() - start_time
    
    print(f"\n⏱️  Total time: {elapsed:.2f} seconds")
    print(f"📊 Average: {elapsed/len(questions):.2f} sec per question")
    
    return answers, elapsed

# ============================================================================
# ASYNCHRONOUS APPROACH (New Way - Fast!)
# ============================================================================

async def ask_claude_async(question):
    """Make an asynchronous Claude API call (non-blocking)"""
    client = anthropic.AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    try:
        response = await client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=300,
            messages=[{"role": "user", "content": question}]
        )
        return response.content[0].text
    finally:
        # Properly close the client
        await client.close()

async def async_example():
    """Ask 5 questions asynchronously (all at once)"""
    questions = [
        "What is async programming in one sentence?",
        "What is a REST API in one sentence?",
        "What is JSON in one sentence?",
        "What is HTTP in one sentence?",
        "What is an API endpoint in one sentence?"
    ]
    
    print("\n🚀 ASYNCHRONOUS APPROACH (All at once)")
    print("="*60)
    
    start_time = time.time()
    
    print(f"  Starting all {len(questions)} requests simultaneously...")
    
    # This is the magic! Run all async functions concurrently
    answers = await asyncio.gather(*[
        ask_claude_async(q) for q in questions
    ])
    
    elapsed = time.time() - start_time
    
    print(f"  ✓ All {len(questions)} answers received!")
    print(f"\n⏱️  Total time: {elapsed:.2f} seconds")
    print(f"📊 Average: {elapsed/len(questions):.2f} sec per question")
    
    return answers, elapsed

# ============================================================================
# COMPARISON & RESULTS
# ============================================================================

def compare_results(sync_time, async_time):
    """Display the performance comparison"""
    print("\n" + "="*60)
    print("📊 PERFORMANCE COMPARISON")
    print("="*60)
    print(f"Synchronous:  {sync_time:.2f} seconds")
    print(f"Asynchronous: {async_time:.2f} seconds")
    print(f"Speedup:      {sync_time/async_time:.1f}x faster!")
    print(f"Time saved:   {sync_time - async_time:.2f} seconds")
    print("="*60)
    
    print("\n💡 KEY INSIGHT:")
    print("Async doesn't make each request faster - it makes multiple")
    print("requests happen at the same time, saving total wall-clock time.")
    print("\nThis is critical for production AI apps!")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

async def main():
    """Main async function"""
    print("\n" + "="*60)
    print("ASYNC vs SYNC PERFORMANCE TEST")
    print("="*60)
    print("We'll ask Claude 5 questions both ways and compare speed.\n")
    
    # Run synchronous version
    sync_answers, sync_time = sync_example()
    
    # Run asynchronous version
    async_answers, async_time = await async_example()
    
    # Compare results
    compare_results(sync_time, async_time)
    
    # Show a sample answer
    print("\n📝 SAMPLE ANSWER (Question 1):")
    print("-"*60)
    print(f"Q: What is async programming in one sentence?")
    print(f"A: {async_answers[0]}")
    print("-"*60)
    
    print("\n✅ Experiment complete!")
    print(f"You just learned how to make your AI apps {sync_time/async_time:.1f}x faster!")

if __name__ == "__main__":
    # Use asyncio.run() which handles event loop creation and cleanup
    asyncio.run(main())
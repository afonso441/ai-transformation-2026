"""
Week 2 Day 3: AI Weather Analyst
Goal: Combine weather data + Claude analysis for intelligent insights
"""

import asyncio
import aiohttp
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

# ============================================================================
# ASYNC WEATHER FETCH (from previous step)
# ============================================================================

async def fetch_weather_async(session, city):
    """Fetch weather for a city"""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric"}
    
    try:
        async with session.get(url, params=params, timeout=10) as response:
            if response.status == 200:
                data = await response.json()
                return {
                    "city": data["name"],
                    "country": data["sys"]["country"],
                    "temp": data["main"]["temp"],
                    "feels_like": data["main"]["feels_like"],
                    "humidity": data["main"]["humidity"],
                    "pressure": data["main"]["pressure"],
                    "description": data["weather"][0]["description"],
                    "wind_speed": data["wind"]["speed"],
                    "clouds": data["clouds"]["all"],
                }
    except Exception as e:
        print(f"❌ Error fetching {city}: {e}")
    
    return None

# ============================================================================
# AI ANALYSIS WITH CLAUDE
# ============================================================================

async def analyze_weather_with_ai(weather_data):
    """
    Send weather data to Claude for intelligent analysis
    
    Claude will provide:
    - Human-readable interpretation
    - What to wear recommendations
    - Activity suggestions
    - Travel/health tips
    """
    
    client = anthropic.AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    # Create a prompt with weather data
    prompt = f"""You are a helpful weather analyst. Analyze this weather data and provide practical advice:

Location: {weather_data['city']}, {weather_data['country']}
Temperature: {weather_data['temp']}°C (feels like {weather_data['feels_like']}°C)
Humidity: {weather_data['humidity']}%
Conditions: {weather_data['description']}
Wind: {weather_data['wind_speed']} m/s
Cloud cover: {weather_data['clouds']}%

Provide:
1. A brief interpretation (2-3 sentences about the weather)
2. What to wear (clothing recommendations)
3. Activity suggestions (indoor vs outdoor)
4. Any health/comfort tips

Be concise, practical, and friendly. Focus on actionable advice."""

    try:
        response = await client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.content[0].text
    
    finally:
        await client.close()

# ============================================================================
# COMPLETE WEATHER ASSISTANT
# ============================================================================

async def get_weather_with_analysis(city):
    """
    Complete workflow:
    1. Fetch weather data (async)
    2. Analyze with AI (async)
    3. Return combined result
    """
    
    print(f"\n{'='*70}")
    print(f"🌤️  WEATHER ANALYSIS FOR {city.upper()}")
    print(f"{'='*70}")
    
    # Step 1: Fetch weather data
    print(f"⏳ Fetching weather data...")
    
    async with aiohttp.ClientSession() as session:
        weather_data = await fetch_weather_async(session, city)
    
    if not weather_data:
        print(f"❌ Could not fetch weather for {city}")
        return None
    
    print(f"✅ Weather data received")
    
    # Display raw data
    print(f"\n📊 CURRENT CONDITIONS:")
    print(f"   Temperature: {weather_data['temp']}°C (feels like {weather_data['feels_like']}°C)")
    print(f"   Conditions: {weather_data['description'].capitalize()}")
    print(f"   Humidity: {weather_data['humidity']}%")
    print(f"   Wind: {weather_data['wind_speed']} m/s")
    print(f"   Cloud cover: {weather_data['clouds']}%")
    
    # Step 2: Get AI analysis
    print(f"\n⏳ Analyzing with AI...")
    
    analysis = await analyze_weather_with_ai(weather_data)
    
    print(f"✅ Analysis complete")
    
    # Display AI insights
    print(f"\n🤖 AI ANALYSIS:")
    print(f"{'-'*70}")
    print(analysis)
    print(f"{'-'*70}")
    
    return {
        "weather": weather_data,
        "analysis": analysis
    }

# ============================================================================
# COMPARE MULTIPLE CITIES WITH AI
# ============================================================================

async def compare_cities_with_ai(cities):
    """
    Fetch weather for multiple cities in parallel,
    then get AI to compare them
    """
    
    print(f"\n{'='*70}")
    print(f"🌍 COMPARING {len(cities)} CITIES")
    print(f"{'='*70}")
    print()
    
    # Fetch all weather data in parallel
    print(f"⏳ Fetching weather for {len(cities)} cities in parallel...")
    
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_weather_async(session, city) for city in cities]
        weather_list = await asyncio.gather(*tasks)
    
    # Filter successful results
    weather_list = [w for w in weather_list if w is not None]
    
    print(f"✅ Fetched {len(weather_list)}/{len(cities)} cities")
    
    # Create comparison prompt
    weather_summary = "\n".join([
        f"- {w['city']}: {w['temp']}°C, {w['description']}, {w['humidity']}% humidity"
        for w in weather_list
    ])
    
    prompt = f"""Compare the weather in these cities and provide travel/living recommendations:

{weather_summary}

Please:
1. Identify which city has the best weather right now
2. Which city would you recommend for outdoor activities?
3. Which city might be uncomfortable (too hot/cold/humid)?
4. Any interesting observations about the weather patterns?

Be concise and practical."""

    # Get AI comparison
    print(f"\n⏳ Getting AI comparison...")
    
    client = anthropic.AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    try:
        response = await client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=600,
            messages=[{"role": "user", "content": prompt}]
        )
        
        comparison = response.content[0].text
    
    finally:
        await client.close()
    
    # Display results
    print(f"\n🤖 AI COMPARISON:")
    print(f"{'-'*70}")
    print(comparison)
    print(f"{'-'*70}")
    
    return comparison

# ============================================================================
# MAIN EXECUTION
# ============================================================================

async def main():
    print("\n" + "="*70)
    print("AI-POWERED WEATHER ANALYST")
    print("="*70)
    
    # Example 1: Single city detailed analysis
    await get_weather_with_analysis("Kuala Lumpur")
    
    # Example 2: Compare multiple cities
    print("\n\n")
    cities_to_compare = [
        "Singapore",
        "Tokyo", 
        "London",
        "Sydney",
        "New York"
    ]
    
    await compare_cities_with_ai(cities_to_compare)
    
    print("\n" + "="*70)
    print("✅ Weather analysis complete!")
    print("="*70)

if __name__ == "__main__":
    asyncio.run(main())
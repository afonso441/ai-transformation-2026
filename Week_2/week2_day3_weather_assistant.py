"""
Week 2 Day 3: Interactive Weather Assistant
Goal: Production-ready CLI tool combining async + APIs + AI
"""

import asyncio
import aiohttp
import anthropic
import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Fix for Windows
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# ============================================================================
# WEATHER FETCHER
# ============================================================================

async def fetch_weather(city):
    """Fetch weather data for a city"""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric"}
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, params=params, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "city": data["name"],
                        "country": data["sys"]["country"],
                        "temp": data["main"]["temp"],
                        "feels_like": data["main"]["feels_like"],
                        "temp_min": data["main"]["temp_min"],
                        "temp_max": data["main"]["temp_max"],
                        "humidity": data["main"]["humidity"],
                        "pressure": data["main"]["pressure"],
                        "description": data["weather"][0]["description"],
                        "wind_speed": data["wind"]["speed"],
                        "clouds": data["clouds"]["all"],
                    }
                elif response.status == 404:
                    return {"error": f"City '{city}' not found"}
                else:
                    return {"error": f"HTTP {response.status}"}
        except asyncio.TimeoutError:
            return {"error": "Request timed out"}
        except Exception as e:
            return {"error": str(e)}

# ============================================================================
# AI ANALYST
# ============================================================================

async def get_ai_analysis(weather_data):
    """Get Claude's analysis of weather data"""
    
    client = anthropic.AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    prompt = f"""Analyze this weather and give practical advice:

📍 {weather_data['city']}, {weather_data['country']}
🌡️  {weather_data['temp']}°C (feels like {weather_data['feels_like']}°C)
💧 Humidity: {weather_data['humidity']}%
☁️  Conditions: {weather_data['description']}
💨 Wind: {weather_data['wind_speed']} m/s

Provide brief, actionable advice:
1. Weather summary (1-2 sentences)
2. What to wear
3. Activity recommendation
4. One helpful tip

Be concise and practical."""

    try:
        response = await client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=400,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    finally:
        await client.close()

# ============================================================================
# DISPLAY
# ============================================================================

def display_weather(weather_data, analysis):
    """Display weather with AI analysis"""
    
    print()
    print("="*70)
    print(f"🌤️  WEATHER IN {weather_data['city'].upper()}, {weather_data['country']}")
    print("="*70)
    print()
    print(f"🌡️  Temperature:  {weather_data['temp']}°C")
    print(f"   Feels like:   {weather_data['feels_like']}°C")
    print(f"   Range:        {weather_data['temp_min']}°C - {weather_data['temp_max']}°C")
    print()
    print(f"💧 Humidity:     {weather_data['humidity']}%")
    print(f"🌀 Pressure:     {weather_data['pressure']} hPa")
    print(f"☁️  Clouds:       {weather_data['clouds']}%")
    print(f"💨 Wind:         {weather_data['wind_speed']} m/s")
    print(f"📝 Conditions:   {weather_data['description'].capitalize()}")
    print()
    print("-"*70)
    print("🤖 AI ANALYSIS:")
    print("-"*70)
    print(analysis)
    print("="*70)
    print()

# ============================================================================
# MAIN ASSISTANT
# ============================================================================

async def weather_assistant():
    """Interactive weather assistant"""
    
    print("\n" + "="*70)
    print("🌤️  AI WEATHER ASSISTANT")
    print("="*70)
    print("Get intelligent weather analysis for any city")
    print("Type 'quit' or 'exit' to stop")
    print("="*70)
    
    while True:
        print()
        city = input("📍 Enter city name (or 'quit'): ").strip()
        
        if city.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Goodbye! Stay weather-aware!")
            break
        
        if not city:
            print("⚠️  Please enter a city name")
            continue
        
        print()
        print(f"⏳ Fetching weather for {city}...")
        
        # Fetch weather
        weather_data = await fetch_weather(city)
        
        # Check for errors
        if "error" in weather_data:
            print(f"❌ Error: {weather_data['error']}")
            continue
        
        print(f"✅ Weather data received")
        print(f"⏳ Analyzing with AI...")
        
        # Get AI analysis
        analysis = await get_ai_analysis(weather_data)
        
        print(f"✅ Analysis complete")
        
        # Display results
        display_weather(weather_data, analysis)

# ============================================================================
# RUN IT
# ============================================================================

if __name__ == "__main__":
    try:
        asyncio.run(weather_assistant())
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted. Goodbye!")
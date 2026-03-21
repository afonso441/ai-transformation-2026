"""
Week 2 Day 3: Async Weather Fetcher
Goal: Fetch weather for multiple cities in parallel
"""

import asyncio
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()

# ============================================================================
# ASYNC WEATHER FETCHER
# ============================================================================

async def fetch_weather_async(session, city):
    """
    Fetch weather for a single city asynchronously
    
    Args:
        session: aiohttp session (reusable connection)
        city: City name
    
    Returns:
        dict: Weather data or None if failed
    """
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }
    
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
                    "description": data["weather"][0]["description"],
                    "wind_speed": data["wind"]["speed"],
                }
            else:
                print(f"❌ {city}: HTTP {response.status}")
                return None
    
    except asyncio.TimeoutError:
        print(f"⏱️  {city}: Timeout")
        return None
    except Exception as e:
        print(f"❌ {city}: {e}")
        return None

async def fetch_multiple_cities(cities):
    """
    Fetch weather for multiple cities in parallel
    
    This is MUCH faster than sequential requests!
    """
    print(f"🌍 Fetching weather for {len(cities)} cities in parallel...")
    print("="*60)
    
    start_time = asyncio.get_event_loop().time()
    
    # Create a shared session (connection pooling)
    async with aiohttp.ClientSession() as session:
        # Create tasks for all cities
        tasks = [fetch_weather_async(session, city) for city in cities]
        
        # Run all tasks concurrently
        results = await asyncio.gather(*tasks)
    
    elapsed = asyncio.get_event_loop().time() - start_time
    
    # Filter out None results (failed requests)
    successful_results = [r for r in results if r is not None]
    
    print(f"✅ Fetched {len(successful_results)}/{len(cities)} cities in {elapsed:.2f}s")
    print(f"📊 Average: {elapsed/len(cities):.2f}s per city")
    print("="*60)
    
    return successful_results

# ============================================================================
# DISPLAY RESULTS
# ============================================================================

def display_weather_summary(weather_list):
    """Display weather data in a nice table"""
    
    if not weather_list:
        print("No weather data to display")
        return
    
    print("\n" + "="*80)
    print("WEATHER SUMMARY")
    print("="*80)
    print(f"{'City':<20} {'Temp':<10} {'Feels':<10} {'Humidity':<12} {'Description':<20}")
    print("-"*80)
    
    for w in weather_list:
        print(f"{w['city']:<20} {w['temp']:>6.1f}°C  {w['feels_like']:>6.1f}°C  "
              f"{w['humidity']:>8}%   {w['description']:<20}")
    
    print("="*80)

# ============================================================================
# TEST IT
# ============================================================================

async def main():
    print("\n" + "="*60)
    print("ASYNC MULTI-CITY WEATHER FETCHER")
    print("="*60)
    print()
    
    # Cities to check
    cities = [
        "Kuala Lumpur",
        "Singapore", 
        "Tokyo",
        "London",
        "New York",
        "Paris",
        "Sydney",
        "Dubai",
        "Mumbai",
        "São Paulo"
    ]
    
    # Fetch all cities in parallel (FAST!)
    weather_data = await fetch_multiple_cities(cities)
    
    # Display results
    display_weather_summary(weather_data)
    
    # Find extremes
    if weather_data:
        hottest = max(weather_data, key=lambda x: x["temp"])
        coldest = min(weather_data, key=lambda x: x["temp"])
        
        print(f"\n🔥 Hottest: {hottest['city']} ({hottest['temp']}°C)")
        print(f"❄️  Coldest: {coldest['city']} ({coldest['temp']}°C)")
        print("="*80)

if __name__ == "__main__":
    asyncio.run(main())
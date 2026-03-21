"""
Week 2 Day 2: Fetch Weather for Multiple Cities
Goal: Practice making multiple API calls efficiently
"""

import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()

def get_weather_simple(city):
    """Simple weather fetch (reusing from earlier)"""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric"}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

def compare_cities(cities):
    """Fetch and compare weather across multiple cities"""
    
    print(f"🌍 COMPARING WEATHER ACROSS {len(cities)} CITIES")
    print("="*70)
    print()
    
    results = []
    
    for city in cities:
        print(f"📍 Fetching: {city}...", end=" ")
        data = get_weather_simple(city)
        
        if data:
            weather = {
                "city": data["name"],
                "country": data["sys"]["country"],
                "temp": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "description": data["weather"][0]["description"]
            }
            results.append(weather)
            print("✅")
        else:
            print("❌")
        
        time.sleep(0.5)  # Be nice to the API
    
    # Display comparison table
    print()
    print("="*70)
    print("WEATHER COMPARISON")
    print("="*70)
    print(f"{'City':<20} {'Temp':<10} {'Humidity':<12} {'Description':<25}")
    print("-"*70)
    
    for w in results:
        print(f"{w['city']:<20} {w['temp']:>6.1f}°C  {w['humidity']:>8}%   {w['description']:<25}")
    
    print("="*70)
    
    # Find extremes
    if results:
        hottest = max(results, key=lambda x: x["temp"])
        coldest = min(results, key=lambda x: x["temp"])
        most_humid = max(results, key=lambda x: x["humidity"])
        
        print()
        print("📊 ANALYSIS:")
        print(f"   🔥 Hottest:      {hottest['city']} ({hottest['temp']}°C)")
        print(f"   ❄️  Coldest:      {coldest['city']} ({coldest['temp']}°C)")
        print(f"   💧 Most humid:   {most_humid['city']} ({most_humid['humidity']}%)")
        print("="*70)
    
    return results

# ============================================================================
# TEST IT
# ============================================================================

if __name__ == "__main__":
    # Cities from different regions
    cities = [
        "Kuala Lumpur",    # Southeast Asia
        "Singapore",       # Southeast Asia
        "Tokyo",           # East Asia
        "Dubai",           # Middle East
        "London",          # Europe
        "New York",        # North America
        "Sydney",          # Australia
        "São Paulo"        # South America
    ]
    
    results = compare_cities(cities)
    
    print("\n✅ Multi-city weather comparison complete!")
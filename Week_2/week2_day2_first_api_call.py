"""
Week 2 Day 2: First REST API Call
Goal: Fetch weather data from OpenWeather API
"""

import requests
import os
from dotenv import load_dotenv

load_dotenv()

# ============================================================================
# SIMPLE API CALL
# ============================================================================

def get_weather_simple(city):
    """
    Fetch current weather for a city
    
    Similar to embedded systems:
    - Send request (like UART TX)
    - Wait for response (like UART RX)
    - Parse response (like parsing protocol bytes)
    """
    
    api_key = os.getenv("OPENWEATHER_API_KEY")
    
    # API endpoint (URL)
    url = "https://api.openweathermap.org/data/2.5/weather"
    
    # Parameters (query string)
    params = {
        "q": city,           # City name
        "appid": api_key,    # Your API key
        "units": "metric"    # Celsius (use "imperial" for Fahrenheit)
    }
    
    print(f"🌐 Calling API for: {city}")
    print(f"   URL: {url}")
    print(f"   Params: q={city}, units=metric")
    print()
    
    # Make HTTP GET request
    response = requests.get(url, params=params)
    
    # Check if request was successful
    if response.status_code == 200:
        # Parse JSON response to Python dict
        data = response.json()
        return data
    else:
        print(f"❌ Error: {response.status_code}")
        print(f"   Message: {response.text}")
        return None

# ============================================================================
# TEST IT
# ============================================================================

if __name__ == "__main__":
    print("="*60)
    print("FIRST REST API CALL")
    print("="*60)
    print()
    
    # Test with your city
    city = "Kuala Lumpur"  # Change to your city!
    
    weather_data = get_weather_simple(city)
    
    if weather_data:
        print("✅ SUCCESS! Received weather data:")
        print("="*60)
        
        # Pretty print the entire JSON response
        import json
        print(json.dumps(weather_data, indent=2))
        
        print("="*60)
        print()
        
        # Extract specific fields
        print("📊 EXTRACTED DATA:")
        print(f"   City: {weather_data['name']}")
        print(f"   Temperature: {weather_data['main']['temp']}°C")
        print(f"   Feels like: {weather_data['main']['feels_like']}°C")
        print(f"   Humidity: {weather_data['main']['humidity']}%")
        print(f"   Description: {weather_data['weather'][0]['description']}")
        print(f"   Wind speed: {weather_data['wind']['speed']} m/s")
        print("="*60)
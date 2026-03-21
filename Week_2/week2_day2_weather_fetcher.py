"""
Week 2 Day 2: Production-Ready Weather Fetcher
Goal: Robust API calls with proper error handling
"""

import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()

# ============================================================================
# PRODUCTION-GRADE API FUNCTION
# ============================================================================

def get_weather(city, max_retries=3):
    """
    Fetch weather with error handling and retries
    
    Returns:
        dict: Weather data if successful
        None: If all retries failed
    """
    
    api_key = os.getenv("OPENWEATHER_API_KEY")
    
    if not api_key:
        print("❌ ERROR: OPENWEATHER_API_KEY not found in .env file")
        return None
    
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }
    
    for attempt in range(max_retries):
        try:
            print(f"🌐 Attempt {attempt + 1}/{max_retries}: Fetching weather for {city}...")
            
            # Add timeout to prevent hanging
            response = requests.get(url, params=params, timeout=10)
            
            # Check HTTP status code
            if response.status_code == 200:
                print("✅ Success!")
                return response.json()
            
            elif response.status_code == 404:
                print(f"❌ City not found: {city}")
                return None  # Don't retry for 404
            
            elif response.status_code == 401:
                print("❌ Invalid API key")
                return None  # Don't retry for auth errors
            
            else:
                print(f"⚠️  HTTP {response.status_code}: {response.text}")
                # Will retry
        
        except requests.exceptions.Timeout:
            print(f"⏱️  Request timed out (>10s)")
        
        except requests.exceptions.ConnectionError:
            print(f"🔌 Connection error (check internet)")
        
        except requests.exceptions.RequestException as e:
            print(f"❌ Request error: {e}")
        
        # Exponential backoff before retry
        if attempt < max_retries - 1:
            wait_time = 2 ** attempt
            print(f"   Waiting {wait_time}s before retry...")
            time.sleep(wait_time)
    
    print(f"❌ Failed after {max_retries} attempts")
    return None

# ============================================================================
# HELPER FUNCTION: FORMAT WEATHER DATA
# ============================================================================

def format_weather(weather_data):
    """
    Extract and format key weather information
    
    Returns a clean dict with just the important fields
    """
    
    if not weather_data:
        return None
    
    try:
        formatted = {
            "city": weather_data["name"],
            "country": weather_data["sys"]["country"],
            "temperature": weather_data["main"]["temp"],
            "feels_like": weather_data["main"]["feels_like"],
            "temp_min": weather_data["main"]["temp_min"],
            "temp_max": weather_data["main"]["temp_max"],
            "humidity": weather_data["main"]["humidity"],
            "pressure": weather_data["main"]["pressure"],
            "description": weather_data["weather"][0]["description"],
            "wind_speed": weather_data["wind"]["speed"],
            "clouds": weather_data["clouds"]["all"],
        }
        
        # Optional fields (might not be present)
        if "rain" in weather_data:
            formatted["rain_1h"] = weather_data["rain"].get("1h", 0)
        
        return formatted
        
    except KeyError as e:
        print(f"❌ Error parsing weather data: missing key {e}")
        return None

# ============================================================================
# DISPLAY WEATHER
# ============================================================================

def display_weather(weather_data):
    """Pretty print weather information"""
    
    if not weather_data:
        print("No weather data to display")
        return
    
    print()
    print("="*60)
    print(f"🌤️  WEATHER IN {weather_data['city'].upper()}, {weather_data['country']}")
    print("="*60)
    print(f"🌡️  Temperature:  {weather_data['temperature']}°C")
    print(f"   Feels like:   {weather_data['feels_like']}°C")
    print(f"   Range:        {weather_data['temp_min']}°C - {weather_data['temp_max']}°C")
    print(f"💧 Humidity:     {weather_data['humidity']}%")
    print(f"🌀 Pressure:     {weather_data['pressure']} hPa")
    print(f"☁️  Clouds:       {weather_data['clouds']}%")
    print(f"💨 Wind:         {weather_data['wind_speed']} m/s")
    print(f"📝 Description:  {weather_data['description'].capitalize()}")
    
    if "rain_1h" in weather_data:
        print(f"🌧️  Rain (1h):    {weather_data['rain_1h']} mm")
    
    print("="*60)
    print()

# ============================================================================
# TEST MULTIPLE CITIES
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("PRODUCTION WEATHER FETCHER")
    print("="*60)
    
    # Test with multiple cities
    cities = [
        "Kuala Lumpur",
        "Singapore",
        "Tokyo",
        "London",
        "New York"
    ]
    
    for city in cities:
        print()
        print("-"*60)
        
        # Fetch weather
        raw_data = get_weather(city)
        
        if raw_data:
            # Format it
            formatted_data = format_weather(raw_data)
            
            # Display it
            display_weather(formatted_data)
        
        # Small delay between requests (be nice to the API)
        time.sleep(1)
    
    print("="*60)
    print("✅ Weather fetching complete!")
    print("="*60)
import argparse
import requests
from dotenv import load_dotenv
import os
import sys

# Load environment variables from .env file
load_dotenv()
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    print("Error: API_KEY is not set. Please add it to your .env file.")
    sys.exit(1)

# API Base URL for WeatherAPI
API_URL = "https://api.weatherapi.com/v1/current.json"

def get_weather_data(city):
    """
    Fetch weather data for a given city using the WeatherAPI.
    """
    try:
        # Construct the API request URL
        params = {
            "key": API_KEY,
            "q": city
        }
        response = requests.get(API_URL, params=params)
        response.raise_for_status()  # Raise an error for HTTP codes >= 400
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        sys.exit(1)

def display_weather(data):
    """
    Display the weather information in a user-friendly format.
    """
    city = data.get("location", {}).get("name")
    country = data["location"].get("country")
    temperature = data["current"].get("temp_c")
    weather = data["current"]["condition"].get("text")
    humidity = data["current"].get("humidity")
    wind_speed = data["current"].get("wind_kph")
    
    print(f"\nWeather in {city}, {country}:")
    print(f"  Temperature: {temperature}°C")
    print(f"  Condition: {weather}")
    print(f"  Humidity: {humidity}%")
    print(f"  Wind Speed: {wind_speed} kph")

def main():
    """
    Main function to handle CLI arguments and run the tool.
    """
    parser = argparse.ArgumentParser(description="Fetch current weather data for a city.")
    parser.add_argument("--city", required=True, help="Name of the city to fetch weather for")
    args = parser.parse_args()

    print(f"Fetching weather data for {args.city}...")
    weather_data = get_weather_data(args.city)
    display_weather(weather_data)

if __name__ == "__main__":
    main()

#%%
from langchain_core.tools import tool
from langchain_community.agent_toolkits import GmailToolkit
import requests
import os

@tool
def get_weather(zip_code: str) -> str:
    """Get current weather conditions for a given US zip code.

    Args:
        zip_code: US zip code of the location
    """
    api_key = os.environ.get('AZURE_MAPS_KEY')
    print('Searching for weather at zip code', zip_code)
    if not api_key:
        raise ValueError("AZURE_MAPS_KEY environment variable is not set")

    # First, convert zip code to coordinates
    geocode_url = f"https://atlas.microsoft.com/search/address/json?api-version=1.0&query={zip_code}&countrySet=US&subscription-key={api_key}"
    geocode_response = requests.get(geocode_url)
    
    if geocode_response.status_code != 200:
        return f"Error geocoding zip code: {geocode_response.status_code}"
    
    geocode_data = geocode_response.json()
    if not geocode_data['results']:
        return f"No location found for zip code {zip_code}"
    
    latitude = geocode_data['results'][0]['position']['lat']
    longitude = geocode_data['results'][0]['position']['lon']

    # Now get the weather using the coordinates
    weather_url = f"https://atlas.microsoft.com/weather/currentConditions/json?api-version=1.1&query={latitude},{longitude}&subscription-key={api_key}&unit=imperial"
    
    weather_response = requests.get(weather_url)
    if weather_response.status_code == 200:
        return weather_response.json()
    else:
        return f"Error fetching weather data: {weather_response.status_code}"

tools = [get_weather]
#tools.append(GmailToolkit().get_tools())

#print(get_weather(47.60357, -122.32945))

# %%

#%%
from langchain_core.tools import tool
import requests
import os

@tool
def add(a: int, b: int) -> int:
    """Add two integers.

    Args:
        a: First integer
        b: Second integer
    """
    print(f"Adding {a} and {b}")
    return a + b

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two integers.

    Args:
        a: First integer
        b: Second integer
    """
    print(f"Multiplying {a} and {b}")
    return a * b

@tool
def subtract(a: int, b: int) -> int:
    """Subtract two integers.

    Args:
        a: First integer
        b: Second integer
    """
    print(f"Subtracting {b} from {a}")
    return a - b

@tool
def get_weather(latitude: float, longitude: float) -> str:
    """Get current weather conditions for a given location.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    api_key = os.environ.get('AZURE_MAPS_KEY')
    print('Searching for weather at', latitude, longitude)
    if not api_key:
        raise ValueError("AZURE_MAPS_KEY environment variable is not set")

    url = f"https://atlas.microsoft.com/weather/currentConditions/json?api-version=1.1&query={latitude},{longitude}&subscription-key={api_key}&unit=imperial"
    
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error fetching weather data: {response.status_code}"

tools = [add, multiply, subtract, get_weather]

#print(get_weather(47.60357, -122.32945))

# %%

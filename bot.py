from discord import Client
from cachetools import TTLCache
import requests
TOKEN = 'e5fecaa7dd6c273fc46ead05e9ad641b38ece36c878e2da1bf9cfd382f070566'
PREFIX = '/'
client=Client()
# Create a cache with a 45-minute TTL (time-to-live)
cache = TTLCache(maxsize=1, ttl=2700)  # 45 minutes in seconds

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith(PREFIX + 'weather'):
        # Check if the response is cached
        cached_response = cache.get(message.author.id)
        if cached_response:
            await message.channel.send(cached_response)
        else:
            location = message.content[len(PREFIX) + len('weather'):].strip()
            if location:
                weather_data = get_weather_data(location)
                if weather_data:
                    emoji = get_weather_emoji(weather_data['current']['weather_descriptions'][0])
                    response = f"Weather in {location}: {emoji} {weather_data['current']['temperature']}°C"
                    cache[message.author.id] = response
                    await message.channel.send(response)
                else:
                    await message.channel.send("Could not fetch weather data for the location.")
            else:
                await message.channel.send("Please provide a location.")

def get_weather_data(location):
    params = {
  'access_key': '38aaeb84517c9020e4bfa56c4ec6e8fe',
  'query': location }

    api_result = requests.get('https://api.weatherstack.com/current', params)

    api_response = api_result.json()
    return api_response

def get_weather_emoji(weather_condition):
    emoji_mapping = {
        'Clear': '☀️',
        'Clouds': '☁️',
        'Rain': '☔',
        'Thunderstorm': '⛈️',
        'Snow': '❄️',
        'Mist': '🌫️',
    }
    return emoji_mapping.get(weather_condition, '🌧️')

client.run(TOKEN)

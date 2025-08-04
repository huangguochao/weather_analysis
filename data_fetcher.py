import requests
import json
import random
import logging
from datetime import datetime

class WeatherFetcher:
    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.api_key = api_key
        self.cache = {}

    def fetch_real_data(self, city):
        try:
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric'
            }
            response = requests.get(self.api_url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            return {
                'city': city,
                'temperature': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        except (requests.RequestException, KeyError) as e:
            logging.error(f"API error for {city}: {e}")
            return None

    def generate_mock_data(self, city):
        return {
            'city': city,
            'temperature': round(random.uniform(-10, 35), 1),
            'humidity': random.randint(30, 100),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

    def get_weather(self, city, use_mock=False):
        if not use_mock:
            data = self.fetch_real_data(city)
            if data:
                return data

        return self.generate_mock_data(city)

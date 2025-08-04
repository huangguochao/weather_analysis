import configparser
import os

class ConfigManager:
    def __init__(self, config_path='config.ini'):
        self.config = configparser.ConfigParser()
        self.config.read(config_path)

        self.output_dir = self.config.get('Paths', 'output_dir')
        os.makedirs(self.output_dir, exist_ok=True)

    def get_api_config(self):
        return {
                'url': self.config.get('API', 'weather_api'),
                'api_key': self.config.get('API', 'api_key')
        }

    def get_db_path(self):
        return self.config.get('Database', 'db_path')

    def get_log_path(self):
        return os.path.join(self.output_dir, self.config.get('Paths', 'log_file'))

    def get_cities(self):
        cities_str = self.config.get('Settings', 'cities')
        return [city.strip() for city in cities_str.split(',')]

    def get_output_dir(self):
        return self.output_dir

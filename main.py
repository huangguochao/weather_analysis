import logging
import time
import argparse
from config import ConfigManager
from database import DatabaseManager
from data_fetcher import WeatherFetcher
from file_manager import FileManager
from data_processor import DataProcessor

def setup_logging(log_path):
    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)s: %(message)s')
    console.setFormatter(formatter)
    logging.getLogger().addHandler(console)

def main():
    parser = argparse.ArgumentParser(description='Weather Data Collection System')
    parser.add_argument('--mock', action='store_true', help='Use mock data instead of real API')
    parser.add_argument('--export', action='store_true', help='Export data to files')
    parser.add_argument('--visualize', action='store_true', help='Generate data visualizations')
    args = parser.parse_args()

    config = ConfigManager()
    setup_logging(config.get_log_path())

    db_manager = DatabaseManager(config.get_db_path())
    api_config = config.get_api_config()
    weather_fetcher = WeatherFetcher(api_config['url'], api_config['api_key'])
    file_manager = FileManager(config.get_output_dir())
    data_processor = DataProcessor(config.get_output_dir())

    logging.info("Starting weather data collection")

    for city in config.get_cities():
        weather_data = weather_fetcher.get_weather(city, args.mock)
        if weather_data:
            db_manager.save_weather_data(
                weather_data['city'],
                weather_data['temperature'],
                weather_data['humidity']
            )
            logging.info(f"Saved data for {city}: "
                         f"{weather_data['temperature']}°C, "
                         f"{weather_data['humidity']}% humidity")
        time.sleep(1)

    if args.export:
        recent_data = db_manager.get_historical_data(limit=100)
        if recent_data:
            csv_path = file_manager.save_to_csv(recent_data, 'recent_weather.csv')
            json_path = file_manager.save_to_json(recent_data, 'recent_weather.json')
            logging.info(f"Data exported to {csv_path} and {json_path}")

        stats = db_manager.get_city_stats()
        if stats:
            report_path = file_manager.save_report(stats, 'weather_report.txt')
            logging.info(f"Report generated at {report_path}")

    if args.visualize:
        for city in config.get_cities():
            city_data = db_manager.get_historical_data(city=city, limit=30)
            if city_data:
                analysis = data_processor.analyze_trends(city_data)
                logging.info(f"{city} temperature analysis: "
                            f"Min={analysis['min']}, Max={analysis['max']}, "
                            f"Avg={analysis['avg']:.1f}, Median={analysis['median']}")

                chart_path = data_processor.visualize_data(city_data, city)
                if chart_path:
                    logging.info(f"Generated chart for {city} at {chart_path}")

    logging.info("Weather data collection completed")

if __name__ == "__main__":
    main()

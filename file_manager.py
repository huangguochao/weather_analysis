import csv
import json
import os
import logging
from datetime import datetime

class FileManager:
    def __init__(self, output_dir):
        self.output_dir = output_dir

    def save_to_csv(self, data, filename):
        filepath = os.path.join(self.output_dir, filename)
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['City', 'Temperature (°C)', 'Humidity (%)', 'Timestamp'])
                for record in data:
                    writer.writerow([
                        record[1], # city
                        record[2], # temperature
                        record[3], # humidity
                        record[4]  # timestamp
                    ])
            return filepath
        except IOError as e:
            logging.error(f"CSV save error: {e}")
            return None

    def save_to_json(self, data, filename):
        filepath = os.path.join(self.output_dir, filename)
        try:
            records = []
            for record in data:
                records.append({
                    'id': record[0],
                    'city': record[1],
                    'temperature': record[2],
                    'humidity': record[3],
                    'timestamp': record[4]
                })

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(records, f, indent=2)
            return filepath
        except IOError as e:
            logging.error(f"JSON save error: {e}")
            return None

    def save_report(self, stats, filename):
        filepath = os.path.join(self.output_dir, filename)
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("Weather Data Analysis Report\n")
                f.write("=" * 40 + "\n")
                f.write(f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

                f.write("{:<15} {:<10} {:<10} {:<10}\n".format(
                    "City", "Avg Temp", "Avg Hum", "Records"))
                f.write("-" * 45 + "\n")

                for stat in stats:
                    f.write("{:<15} {:<10.1f} {:<10.1f} {:<10}\n".format(
                        stat[0], stat[1], stat[2], stat[3]))
            return filepath
        except IOError as e:
            logging.error(f"Report save error: {e}")
            return None

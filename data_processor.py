import numpy as np
import matplotlib.pyplot as plt
import logging
import os

class DataProcessor:
    def __init__(self, output_dir):
        self.output_dir = output_dir

    def analyze_trends(self, data):
        if not data:
            return None

        temperatures = [record[2] for record in data]

        return {
            'min': min(temperatures),
            'max': max(temperatures),
            'avg': sum(temperatures) / len(temperatures),
            'median': sorted(temperatures)[len(temperatures) // 2]
        }

    def visualize_data(self, data, city):
        if not data:
            return None

        timestamps = [record[4][:10] for record in data]
        temperatures = [record[2] for record in data]

        plt.figure(figsize=(10, 6))
        plt.plot(timestamps, temperatures, 'o-')
        plt.title(f'Temperature Trend in {city}')
        plt.xlabel('Date')
        plt.ylabel('Temperature (°C)')
        plt.xticks(rotation=45)
        plt.grid(True, linestyle='--', alpha=0.7)

        filename = f"{city.replace(' ', '_')}_trend.png"
        filepath = os.path.join(self.output_dir, filename)
        plt.tight_layout()
        plt.savefig(filepath)
        plt.close()

        return filepath

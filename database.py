import sqlite3
import logging

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None
        self._create_table()

    def _create_table(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS weather (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        city TEXT NOT NULL,
                        temperature REAL NOT NULL,
                        humidity INTEGER NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Database error: {e}")

    def save_weather_data(self, city, temperature, humidity):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO weather (city, temperature, humidity)
                    VALUES (?, ?, ?)
                ''', (city, temperature, humidity))
                conn.commit()
                return True
        except sqlite3.Error as e:
            logging.error(f"Error saving data: {e}")
            return False

    def get_historical_data(self, city=None, limit=100):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                if city:
                    cursor.execute('''
                        SELECT * FROM weather
                        WHERE city = ?
                        ORDER BY timestamp DESC
                        LIMIT ?
                    ''', (city, limit))
                else:
                    cursor.execute('''
                        SELECT * FROM weather
                        ORDER BY timestamp DESC
                        LIMIT ?
                    ''', (limit,))
                return cursor.fetchall()
        except sqlite3.Error as e:
            logging.error(f"Error fetching data: {e}")
            return []

    def get_city_stats(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT city,
                            AVG(temperature) as avg_temp,
                            AVG(humidity) as avg_humidity,
                            COUNT(*) as records
                    FROM weather
                    GROUP BY city
                ''')
                return cursor.fetchall()
        except sqlite3.Error as e:
            logging.error(f"Error fetching stats: {e}")
            return []

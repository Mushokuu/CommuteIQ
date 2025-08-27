import json
import time
import requests
import sqlite3
from datetime import datetime, timezone

# You must install this library first: pip install gtfs-realtime-bindings
from google.transit import gtfs_realtime_pb2

# --- CONFIGURATION ---

DB_FILE = "transport_data.db"

# 1. Get your free API key from: https://otd.delhi.gov.in/data/realtime/
# 2. Replace "YOUR_API_KEY_HERE" with the key you receive.
DELHI_OTD_API_KEY = "YOUR_API_KEY"

# Replace with your own free API key from OpenWeatherMap
# Sign up here: https://openweathermap.org/appid
OPENWEATHERMAP_API_KEY = "YOUR_API_KEY" 
DELHI_COORDS = {"lat": 28.7041, "lon": 77.1025}

# Add headers to make requests look like they're from a browser
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# --- DATABASE SETUP ---

def setup_database():
    """
    Creates the SQLite database and the necessary tables if they don't exist.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Create table for bus locations
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bus_locations (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_id TEXT NOT NULL,
            route_id TEXT,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            speed REAL,
            timestamp TEXT NOT NULL
        )
    ''')

    # Create table for weather data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather_logs (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            temperature REAL,
            feels_like REAL,
            humidity INTEGER,
            wind_speed REAL,
            condition TEXT,
            description TEXT,
            scraped_at TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"Database '{DB_FILE}' is set up and ready.")

# --- LIVE DATA FETCHING ---

def fetch_delhi_live_bus_data():
    """
    Fetches, parses, and cleans the GTFS-Realtime feed from Delhi's OTD portal.
    """
    if DELHI_OTD_API_KEY == "YOUR_API_KEY_HERE":
        print("ERROR: Delhi OTD API key is not set.")
        return None

    url = f"https://otd.delhi.gov.in/api/realtime/VehiclePositions.pb?key={DELHI_OTD_API_KEY}"
    locations = []
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(response.content)
        current_scrape_time = datetime.now(timezone.utc).isoformat()

        for entity in feed.entity:
            if entity.HasField('vehicle'):
                vehicle = entity.vehicle
                position = vehicle.position
                if position.latitude == 0.0 or position.longitude == 0.0:
                    continue
                locations.append({
                    "vehicle_id": vehicle.vehicle.id,
                    "route_id": vehicle.trip.route_id,
                    "latitude": position.latitude,
                    "longitude": position.longitude,
                    "speed": position.speed if position.HasField('speed') else None,
                    "timestamp": current_scrape_time
                })
        return locations

    except requests.exceptions.RequestException as e:
        print(f"Error fetching Delhi live bus data: {e}")
        return None
    except Exception as e:
        print(f"Error parsing GTFS data: {e}")
        return None

def fetch_weather_data():
    """
    Fetches REAL live weather data from the OpenWeatherMap API for Delhi.
    """
    if OPENWEATHERMAP_API_KEY == "YOUR_API_KEY_HERE":
        print("WARNING: OpenWeatherMap API key not set.")
        return None
        
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={DELHI_COORDS['lat']}&lon={DELHI_COORDS['lon']}&appid={OPENWEATHERMAP_API_KEY}&units=metric"
    
    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        data = response.json()
        return {
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "condition": data["weather"][0]["main"],
            "description": data["weather"][0]["description"],
            "scraped_at": datetime.now(timezone.utc).isoformat()
        }
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

# --- DATA STORAGE ---

def save_data_to_db(bus_data, weather_data):
    """
    Saves the fetched bus and weather data into the SQLite database.
    """
    if not bus_data and not weather_data:
        return

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Insert bus data
    if bus_data:
        bus_rows = [(d['vehicle_id'], d['route_id'], d['latitude'], d['longitude'], d['speed'], d['timestamp']) for d in bus_data]
        cursor.executemany('''
            INSERT INTO bus_locations (vehicle_id, route_id, latitude, longitude, speed, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', bus_rows)
        print(f"-> Saved {len(bus_rows)} bus records to the database.")

    # Insert weather data
    if weather_data:
        weather_tuple = (
            weather_data['temperature'], weather_data['feels_like'], weather_data['humidity'],
            weather_data['wind_speed'], weather_data['condition'], weather_data['description'],
            weather_data['scraped_at']
        )
        cursor.execute('''
            INSERT INTO weather_logs (temperature, feels_like, humidity, wind_speed, condition, description, scraped_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', weather_tuple)
        print("-> Saved 1 weather record to the database.")

    conn.commit()
    conn.close()

# --- MAIN SCRIPT ---

def main():
    """
    Main loop to continuously fetch, display, and save data.
    """
    setup_database()
    print("\nStarting Live Delhi Public Transport Data Scraper...")
    print("This script will fetch and save data every 60 seconds. Press Ctrl+C to stop.")
    
    while True:
        bus_data = fetch_delhi_live_bus_data()
        weather_data = fetch_weather_data()
        
        if bus_data is None:
            print("Halting due to a critical error during data fetching. Please check the logs above.")
            break

        print("\n" + "="*50)
        print(f"Data fetched at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Found {len(bus_data)} live buses with valid locations.")
        
        # Save the data to the database
        save_data_to_db(bus_data, weather_data)
        print("="*50)
        
        time.sleep(60)

if __name__ == "__main__":
    main()

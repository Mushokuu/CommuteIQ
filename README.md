# Real-Time Public Transport Forecaster for Delhi

This project is an end-to-end data pipeline that acquires live public transit data for Delhi, analyzes historical patterns, and uses a machine learning model to recommend the optimal travel time for any bus route, taking future weather conditions into account.

## 🚀 Project Objective

The goal of this project is to solve a common urban mobility challenge: predicting bus travel times in a city with dynamic traffic and weather. The application provides a smart recommendation engine that helps users decide the best time to start their journey to minimize travel duration.

## 🌟 Key Features

- **Live Data Ingestion**: Connects to Delhi's official GTFS-Realtime API to fetch live bus locations every minute.

- **Data Enrichment**: Enriches the transit data with both current and forecasted weather conditions from the OpenWeatherMap API.

- **Automated Data Cleaning**: Includes a robust cleaning layer to filter out invalid real-world data (e.g., buses reporting 0,0 coordinates).

- **Persistent Storage**: Stores all historical data in a lightweight SQLite database, building a valuable dataset over time.

- **Advanced SQL Analysis**: A dedicated module runs complex SQL queries (using JOINS, Aggregations, and Window Functions) to derive historical insights.

- **ML-Powered Recommendations**: Uses a trained scikit-learn model to predict travel times and recommend the optimal departure window based on future weather forecasts.

- **Terminal-Based UI**: A simple, clean command-line interface makes the analysis and predictions easily accessible.

## 🛠️ Tech Stack

- **Language**: Python
- **Data Science & ML**: scikit-learn, Pandas
- **Data Engineering & APIs**: REST APIs, GTFS-Realtime, Requests
- **Database**: SQL, SQLite

## ⚙️ Project Architecture

The application is built as a 3-step data pipeline:

1. **Data Acquisition & Ingestion** (`transport_scraper_live.py`): A script runs continuously to fetch, clean, enrich, and store live bus and weather data.

2. **Data Storage & Analysis** (`analyze_data.py`): A SQLite database stores the historical data, which can be queried by a dedicated analysis script to uncover patterns.

3. **Predictive Modeling & UI** (`app.py` - to be built): A machine learning model is trained on the historical data. A terminal application provides the user interface to get travel time recommendations.

## 🏁 Getting Started

### Prerequisites

- Python 3.8+
- pip (Python package installer)

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd <your-repository-name>
```

### 2. Install Dependencies

Create a `requirements.txt` file with the following content:

```txt
requests
pandas
scikit-learn
gtfs-realtime-bindings
```

Then, install the packages:

```bash
pip install -r requirements.txt
```

### 3. Set Up API Keys

You will need two free API keys:

- **Delhi OTD Key**: Get it from [Open Transit Data Delhi](https://otd.delhi.gov.in/)
- **OpenWeatherMap Key**: Get it from [OpenWeatherMap](https://openweathermap.org/api)

Open `transport_scraper_live.py` and replace the placeholder values for `DELHI_OTD_API_KEY` and `OPENWEATHERMAP_API_KEY`.

### 4. Run the Application

#### Step A: Collect Data

First, you need to collect data. Run the scraper for at least a few hours (ideally 24+) to build a solid dataset.

```bash
python transport_scraper_live.py
```

This will create a `transport_data.db` file and start populating it.

#### Step B: Run Historical Analysis (Optional)

To see insights from the data you've collected, run the analysis script.

```bash
python analyze_data.py
```

#### Step C: Get a Travel Recommendation

Once the main application is built, you will run it to get predictions.

```bash
python app.py
```

## 📊 Sample Output

The final application will provide a clear recommendation in the terminal:

```
------------------------------------------------------------------
Travel Time Forecast for Route 548 in the Next 6 Hours:

- 02:00 PM: ~45 mins (Forecast: Rain)
- 02:30 PM: ~48 mins (Forecast: Rain)
- 03:00 PM: ~42 mins (Forecast: Clouds)
- 03:30 PM: ~35 mins (Forecast: Clear)
- 04:00 PM: ~33 mins (Forecast: Clear)
- 04:30 PM: ~38 mins (Forecast: Clear) <-- Traffic increasing
- 05:00 PM: ~43 mins (Forecast: Clear) <-- Evening peak begins

RECOMMENDATION: The optimal time to travel is around 04:00 PM.
------------------------------------------------------------------
```

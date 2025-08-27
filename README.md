This project is an end-to-end data pipeline that acquires live public transit data for Delhi, analyzes patterns, and uses a machine learning model to recommend the optimal travel time for any bus route, taking future weather conditions into account.

🚀 Project Objective

The goal is to solve a common urban mobility challenge: predicting bus travel times in a city with dynamic traffic and weather. The application provides a recommendation engine that helps users decide the best time to start their journey to minimize travel duration.

🌟 Key Features

Live Data Ingestion: Connects to Delhi's official GTFS-Realtime API to fetch live bus locations every minute.

Data Enrichment: Enriches transit records with current and forecasted weather from OpenWeatherMap.

Automated Data Cleaning: Filters invalid real-world data (e.g., GPS pings at 0,0) and normalizes timestamps.

Persistent Storage: Stores collected RT data in a lightweight SQLite database, building a dataset over time.

Advanced SQL Analysis: A module runs optimized SQL queries (joins, aggregations, window functions) to surface commuter insights.

ML-Powered Recommendations: A scikit-learn model predicts travel times and recommends optimal departure windows based on forecasted weather.

Terminal-Based UI: A minimal CLI exposes predefined, SQL-backed commuter reports and ML forecasts.

🛠️ Tech Stack

Language: Python

Data Science & ML: scikit-learn, pandas

APIs / Ingestion: REST APIs, GTFS-Realtime, requests

Database / Querying: SQLite, SQL

⚙️ Project Architecture

The app is implemented as a 3-step pipeline:

Data Acquisition & Ingestion (transport_scraper_live.py) — continuously fetches GTFS-Realtime and weather feeds, cleans records, and persists valid pings.

Data Storage & Analysis (analyze_data.py) — stores pings and weather snapshots in transport_data.db and runs SQL analysis to extract patterns.

Predictive Modeling & UI (app.py — to be built) — trains the ML model on stored RT data and exposes a terminal UI for forecasts and insights.

🏁 Getting Started
Prerequisites

Python 3.8+

pip

1. Clone the repository

git clone <your-repository-url>
cd <your-repository-name>

2. Install dependencies

pip install -r requirements.txt
(Include requests, pandas, scikit-learn, gtfs-realtime-bindings in requirements.txt)

3. Set up API keys

You will need two API credentials:

Delhi OTD Key: obtain from Open Transit Data Delhi.

OpenWeatherMap Key: obtain from OpenWeatherMap.

Open transport_scraper_live.py (or configure .env) and replace the placeholder values for DELHI_OTD_API_KEY and OPENWEATHERMAP_API_KEY.

4. Run the application

Step A — Collect data
Run the scraper to build data: python transport_scraper_live.py
(Collect for several hours — ideally 24+ — to get a reliable dataset.)
This creates transport_data.db and begins populating it.

Step B — Run historical analysis (optional)
Run the analysis to view SQL reports: python analyze_data.py

Step C — Get travel recommendations
When app.py is available, run: python app.py

📊 Sample Output

Travel Time Forecast for Route 548 in the Next 6 Hours:

02:00 PM: ~45 mins (Forecast: Rain)

02:30 PM: ~48 mins (Forecast: Rain)

03:00 PM: ~42 mins (Forecast: Clouds)

03:30 PM: ~35 mins (Forecast: Clear)

04:00 PM: ~33 mins (Forecast: Clear)

04:30 PM: ~38 mins (Forecast: Clear) ← traffic increasing

05:00 PM: ~43 mins (Forecast: Clear) ← evening peak begins

RECOMMENDATION: The optimal time to travel is around 04:00 PM.

📂 Project Structure

data/ — raw and processed snapshots (optional)

models/ — trained ML models and preprocessing artifacts

notebooks/ — EDA and experiments

scripts/ or root scripts:

transport_scraper_live.py — ingestion & cleaning

analyze_data.py — SQL analytics

train_model.py — feature engineering & training

predict.py — inference utilities

app.py / commuteiq_cli.py — terminal UI (user entrypoints)

transport_data.db — example/generated SQLite DB

requirements.txt

README.md

🔮 Roadmap / Future Work

Migrate to PostgreSQL for scalability and concurrency.

Expose ML predictions via a REST API (FastAPI) and add a web dashboard (Streamlit / React).

Add visualization: interactive maps, time-series charts.

Extend to multi-modal support (metro, trains).

Experiment with deep time-series models (LSTM / Transformer) and probabilistic forecasts.

Add alerting (email/SMS) for significant delays.

📚 Learnings & Notes

Real-time feeds are noisy — robust validation and anomaly handling are critical.

Schema design in SQLite matters for query performance even in small deployments.

Thoughtful feature engineering (rolling speeds, cyclic time encodings) often outperforms complex models.

Use time-based train/test splits to avoid data leakage.

Combining weather, recent speeds, and temporal signals improves prediction reliability.

🤝 Contributing

Contributions welcome. Typical workflow: fork → branch → PR. Include tests and update docs for notable changes.

⚖️ License

MIT License — see LICENSE for details.

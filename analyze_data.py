import sqlite3
import pandas as pd

# --- CONFIGURATION ---
DB_FILE = "transport_data.db"

def run_query(conn, query, description):
    """A helper function to run a query and print the results."""
    print(f"--- {description} ---")
    try:
        df = pd.read_sql_query(query, conn)
        if df.empty:
            print("No results found for this query.")
        else:
            # pd.to_string() prints the entire DataFrame without truncation
            print(df.to_string())
    except Exception as e:
        print(f"An error occurred: {e}")
    print("\n" + "="*60 + "\n")

def perform_analysis():
    """
    Connects to the database and runs a series of complex SQL queries for analysis.
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        print(f"Successfully connected to '{DB_FILE}' for analysis.\n")

        # --- Query 1: Bus Activity by Hour of the Day ---
        # This query counts the number of unique buses reporting their location for each hour.
        # It uses strftime to extract the hour from the timestamp.
        q1_description = "Bus Activity by Hour of the Day"
        q1_query = """
            SELECT
                strftime('%H', timestamp) AS hour_of_day,
                COUNT(DISTINCT vehicle_id) AS active_buses
            FROM
                bus_locations
            GROUP BY
                hour_of_day
            ORDER BY
                hour_of_day;
        """
        run_query(conn, q1_query, q1_description)

        # --- Query 2: Top 10 Busiest Bus Routes ---
        # This query finds the routes with the most unique buses operating on them.
        q2_description = "Top 10 Busiest Bus Routes"
        q2_query = """
            SELECT
                route_id,
                COUNT(DISTINCT vehicle_id) AS unique_bus_count
            FROM
                bus_locations
            WHERE
                route_id IS NOT NULL
            GROUP BY
                route_id
            ORDER BY
                unique_bus_count DESC
            LIMIT 10;
        """
        run_query(conn, q2_query, q2_description)

        # --- Query 3: Average Bus Speed by Weather Condition ---
        # This is a complex query that joins the two tables on a rounded timestamp.
        # It shows how external factors (weather) might influence operations.
        q3_description = "Average Bus Speed by Weather Condition"
        q3_query = """
            SELECT
                w.condition,
                AVG(b.speed) AS average_speed_kmh,
                COUNT(b.vehicle_id) as data_points
            FROM
                bus_locations b
            JOIN
                weather_logs w ON strftime('%Y-%m-%d %H:%M', b.timestamp) = strftime('%Y-%m-%d %H:%M', w.scraped_at)
            WHERE
                b.speed IS NOT NULL AND b.speed > 0
            GROUP BY
                w.condition
            ORDER BY
                average_speed_kmh DESC;
        """
        run_query(conn, q3_query, q3_description)

        # --- Query 4: Identifying Potentially 'Stuck' Buses ---
        # This advanced query uses a Common Table Expression (CTE) and the LAG() window function.
        # It finds buses that reported the exact same coordinates for two consecutive readings.
        q4_description = "Buses Stationary for Consecutive Readings (Potentially Stuck)"
        q4_query = """
            WITH BusJourneys AS (
                SELECT
                    vehicle_id,
                    latitude,
                    longitude,
                    timestamp,
                    LAG(latitude, 1, 0) OVER (PARTITION BY vehicle_id ORDER BY timestamp) AS prev_lat,
                    LAG(longitude, 1, 0) OVER (PARTITION BY vehicle_id ORDER BY timestamp) AS prev_lon
                FROM
                    bus_locations
            )
            SELECT
                vehicle_id,
                latitude,
                longitude,
                timestamp
            FROM
                BusJourneys
            WHERE
                latitude = prev_lat AND longitude = prev_lon
            ORDER BY
                vehicle_id, timestamp DESC
            LIMIT 10;
        """
        run_query(conn, q4_query, q4_description)

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if 'conn' in locals() and conn:
            conn.close()
            print(f"Analysis complete. Connection to '{DB_FILE}' closed.")

if __name__ == "__main__":
    # You will need to install pandas: pip install pandas
    perform_analysis()

import os
import requests
import snowflake.connector
from dotenv import load_dotenv


load_dotenv()


CITIES = [
    {"city": "Cologne", "latitude": 50.94, "longitude": 6.96},
    {"city": "Istanbul", "latitude": 41.01, "longitude": 28.97},
    {"city": "London", "latitude": 51.50, "longitude": -0.12},
]


def fetch_temperature(latitude, longitude):
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}&longitude={longitude}&current=temperature_2m"
    )

    response = requests.get(url)
    response.raise_for_status()

    data = response.json()
    return data["current"]["temperature_2m"]


def connect_to_snowflake():
    return snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
    )


def insert_weather_data(cursor, city, temperature):
    cursor.execute(
        """
        INSERT INTO weather_data (city, temperature, recorded_at)
        VALUES (%s, %s, CURRENT_TIMESTAMP())
        """,
        (city, temperature),
    )


def main():
    conn = connect_to_snowflake()
    cursor = conn.cursor()

    try:
        for city_config in CITIES:
            city = city_config["city"]
            temperature = fetch_temperature(
                city_config["latitude"],
                city_config["longitude"]
            )

            insert_weather_data(cursor, city, temperature)
            print(f"Inserted {city}: {temperature}°C")

        conn.commit()
        print("Weather data ingestion completed successfully.")

    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    main()
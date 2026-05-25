import requests
import snowflake.connector
import os
from dotenv import load_dotenv

load_dotenv()

print("USER:", os.getenv("SNOWFLAKE_USER"))
print("ACCOUNT:", os.getenv("SNOWFLAKE_ACCOUNT"))

response = requests.get(
    "https://api.open-meteo.com/v1/forecast?latitude=50.94&longitude=6.96&current=temperature_2m"
)

data = response.json()

temperature = data["current"]["temperature_2m"]

print(temperature)

conn = snowflake.connector.connect(
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA")
)

print("Connected to Snowflake")

cur = conn.cursor()

cur.execute(
    """
    INSERT INTO weather_data (city, temperature, recorded_at)
    VALUES (%s, %s, CURRENT_TIMESTAMP())
    """,
    ("Cologne", temperature)
)

conn.commit()

cur.close()
conn.close()

print("Inserted weather data into Snowflake")
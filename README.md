# Snowflake Weather Data Pipeline

Mini data engineering project built to develop hands-on Snowflake platform engineering skills.

## Project Overview

This project demonstrates a simple end-to-end data pipeline:

- Fetch live weather data from a public API
- Process data with Python
- Connect securely to Snowflake using environment variables
- Ingest raw data into Snowflake
- Transform raw data into an analytics-ready layer using SQL

## Architecture

```text
Weather API
   ↓
Python ingestion script
   ↓
Snowflake RAW layer
   ↓
SQL transformation
   ↓
Analytics layer
```

## Technologies Used

- Python
- Snowflake
- Snowflake Python Connector
- SQL
- REST API
- dotenv
- Git / GitHub

## Project Structure

```text
snowflake-weather-platform/
├── weather_ingestion.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Data Flow

### 1. Data Extraction
The Python script fetches current weather data from the Open-Meteo API.

### 2. Data Ingestion
The script connects to Snowflake and inserts weather data into the RAW table:

```sql
raw.weather_data
```

### 3. Data Transformation
A SQL transformation creates the latest analytics-ready weather view:

```sql
analytics.weather_latest
```

using window functions (`ROW_NUMBER`, `PARTITION BY`) to keep only the newest record per city.

## Security

Sensitive credentials are stored in a local `.env` file and excluded from version control using `.gitignore`.

## Future Improvements

- Support multiple cities dynamically
- Add scheduling / automation
- Add Docker support
- Add CI/CD pipeline
- Add dbt transformations
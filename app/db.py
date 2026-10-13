# This file will handle db connections

from supabase import create_client
from dotenv import load_dotenv
from clean_mushroom_data import get_geodataframe
from clean_weather_data import get_weather_data, get_station_data
from ml import predictions_for_db
import numpy as np
import os

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SECRET_KEY = os.getenv("SUPABASE_SECRET_KEY")

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_SECRET_KEY
)

def put_to_db(observations):
    response = (
        supabase.table("observations").insert(observations).execute()
    )
    return response

def read_from_db():
    response = (
        supabase.table("observations").select("*").execute()
    )
    return response.data

def put_weather_to_db(weather):
    return (
        supabase.table("weather").insert(weather).execute()
    )

def read_weather():
    return (
        supabase.table("weather").select("*").execute()
    ).data

def seed_database():

    df = get_geodataframe()

    df = df.drop(columns=["geometry"])
    
    df = df.rename(columns={
    "Species": "species",
    "Vernacular name": "vernacular_name",
    "Time": "observation_time",
    "WGS84 N": "wgs84_n",
    "WGS84 E": "wgs84_e"
    })

    df["observation_time"] = df["observation_time"].dt.strftime("%Y-%m-%d")

    observations = df[
        [
        "species",
        "vernacular_name",
        "observation_time",
        "wgs84_n",
        "wgs84_e"
        ]
    ].to_dict(orient="records")

    response = put_to_db(observations)

    print(f"Uploaded {len(observations)} observations")

    return response


def upload_weather_batches(records, batch_size=500):
        for i in range(0, len(records), batch_size):
            batch = records[i:i + batch_size]

            supabase.table("weather").insert(batch).execute()

            print(f"Uploaded {min(i + batch_size, len(records))} / {len(records)}")

def seed_weather_database():
    df = get_weather_data()
    
    df["time"] = df["time"].dt.strftime("%Y-%m-%d")
    df = df.replace({np.nan: None})

    weather_records = df.to_dict(orient="records")

    upload_weather_batches(weather_records)

    print(f"Uploaded {len(weather_records)} weather records")



def seed_stations_database():
    df = get_station_data()

    df = df.drop(columns=["geometry"])

    stations = df.to_dict(orient="records")

    supabase.table("stations").insert(stations).execute()

    print(f"Uploaded {len(stations)} stations")
    
    

def upload_predictions_batches(records, batch_size=500):
    for i in range(0, len(records), batch_size):
        batch = records[i:i + batch_size]
        supabase.table("predictions").upsert(batch, on_conflict="species,grid_x,grid_y,week").execute()
        print(f"Uploaded {min(i + batch_size, len(records))} / {len(records)}")
            
    
def seed_predictions_database():
    df = predictions_for_db()
    records = df.to_dict(orient="records")
    upload_predictions_batches(records)
    print(f"Uploaded {len(records)} weather records")
    
def read_predictions():
    response = (
        supabase.table("predictions").select("*").eq("species", "herkkutatti").execute()
    )
    print(response.data)
    return response.data

if __name__ == "__main__":
    # seed_database()
    # seed_stations_database()
    # seed_weather_database()
    seed_predictions_database()
    # read_predictions()
    
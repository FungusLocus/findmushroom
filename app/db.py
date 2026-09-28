# This file will handle db connections

from supabase import create_client
from dotenv import load_dotenv
from clean_mushroom_data import get_dataframe
import os

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
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

def seed_database():

    df = get_dataframe()
    
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

if __name__ == "__main__":
    seed_database()
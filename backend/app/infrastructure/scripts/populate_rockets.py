# app/infrastructure/scripts/populate_data.py
import requests
from sqlmodel import create_engine, Session
from app.infrastructure.scripts.rocket_loader import fetch_and_load_rockets, fetch_and_load_launches, fetch_and_load_starlinks
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def main():
    engine = create_engine(DATABASE_URL, echo=True)
    SPACEX_ROCKETS_URL = "https://api.spacexdata.com/v4/rockets"
    SPACEX_LAUNCHES_URL = "https://api.spacexdata.com/v4/launches"
    SPACEX_STARLINK_URL = "https://api.spacexdata.com/v4/starlink"

    with Session(engine) as session:
        # Fetch and load rockets
        response = requests.get(SPACEX_ROCKETS_URL)
        response.raise_for_status()
        rockets_data = response.json()
        fetch_and_load_rockets(session, rockets_data)

        # Fetch and load launches
        response = requests.get(SPACEX_LAUNCHES_URL)
        response.raise_for_status()
        launches_data = response.json()
        fetch_and_load_launches(session, launches_data)

        # Fetch and load starlinks
        response = requests.get(SPACEX_STARLINK_URL)
        response.raise_for_status()
        starlinks_data = response.json()
        fetch_and_load_starlinks(session, starlinks_data)

if __name__ == "__main__":
    main()
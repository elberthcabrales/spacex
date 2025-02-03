# app/infrastructure/scripts/rocket_loader.py
import requests
from sqlmodel import Session

from app.core.domain.rocket import Rocket
from app.core.domain.first_stage import FirstStage
from app.core.domain.second_stage import SecondStage

SPACEX_ROCKETS_URL = "https://api.spacexdata.com/v4/rockets"

def fetch_and_load_rockets(session: Session) -> None:
    """
    Fetch rocket data from SpaceX API and insert into the database,
    including first_stage and second_stage info.
    """
    response = requests.get(SPACEX_ROCKETS_URL)
    response.raise_for_status()
    rockets_data = response.json()

    print(f"Found {len(rockets_data)} rockets")

    for item in rockets_data:
        # Map fields from the API response to our Rocket model
        rocket = Rocket(
            rocket_uuid=item["id"],
            name=item.get("name"),
            active=item.get("active"),
            stages=item.get("stages"),
            cost_per_launch=item.get("cost_per_launch"),
            first_flight=item.get("first_flight"),
            country=item.get("country"),
            description=item.get("description"),
            wikipedia=item.get("wikipedia"),
            # Convert the nested "height" and "diameter" to float (meters)
            height=float(item["height"]["meters"]) if item["height"]["meters"] else None,
            diameter=float(item["diameter"]["meters"]) if item["diameter"]["meters"] else None,
            # The 'mass' is a dict with kg. We'll store it as text (e.g., "540000")
            weight=str(item["mass"]["kg"]) if item["mass"]["kg"] else None,
        )
        session.add(rocket)

        # Extract first stage fields
        first_stage_data = item.get("first_stage", None)
        if first_stage_data:
            # Create a FirstStage record referencing the rocket_uuid
            first_stage = FirstStage(
                reusable=first_stage_data.get("reusable"),
                engines=first_stage_data.get("engines"),
                fuel_amount_tons=first_stage_data.get("fuel_amount_tons"),
                burn_time_sec=first_stage_data.get("burn_time_sec"),
                rocket_uuid=rocket.rocket_uuid,  # links to the same rocket
            )
            session.add(first_stage)

        # Extract second stage fields
        second_stage_data = item.get("second_stage")
        if second_stage_data:
            # Create a SecondStage record referencing the rocket_uuid
            second_stage = SecondStage(
                reusable=second_stage_data.get("reusable"),
                engines=second_stage_data.get("engines"),
                fuel_amount_tons=second_stage_data.get("fuel_amount_tons"),
                rocket_uuid=rocket.rocket_uuid,
            )
            session.add(second_stage)

    # Commit everything after the loop
    session.commit()
    print("Rocket, FirstStage, and SecondStage data inserted successfully.")

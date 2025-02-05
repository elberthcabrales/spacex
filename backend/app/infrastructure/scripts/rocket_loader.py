# app/infrastructure/scripts/rocket_loader.py
import requests
from sqlmodel import Session
from app.core.domain.failure import Failure
from app.core.domain.rocket import Rocket
from app.core.domain.first_stage import FirstStage
from app.core.domain.second_stage import SecondStage
from app.core.domain.launch import Launch
from app.core.domain.starlink import Starlink

SPACEX_ROCKETS_URL = "https://api.spacexdata.com/v4/rockets"
SPACEX_LAUNCHES_URL = "https://api.spacexdata.com/v4/launches"
SPACEX_STARLINK_URL = "https://api.spacexdata.com/v4/starlink"

def fetch_and_load_rockets(session: Session) -> None:
    """
    Fetch rocket data from SpaceX API and insert into the database,
    including first_stage and second_stage info.
    """
    try:
        response = requests.get(SPACEX_ROCKETS_URL)
        response.raise_for_status()
        rockets_data = response.json()

        print(f"Found {len(rockets_data)} rockets")

        for item in rockets_data:
            # Insert Rocket
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
                height=float(item["height"]["meters"]) if item["height"]["meters"] else None,
                diameter=float(item["diameter"]["meters"]) if item["diameter"]["meters"] else None,
                weight=str(item["mass"]["kg"]) if item["mass"]["kg"] else None,
            )
            session.merge(rocket)

            # Insert FirstStage (one-to-one)
            first_stage_data = item.get("first_stage")
            if first_stage_data:
                first_stage = FirstStage(
                    reusable=first_stage_data.get("reusable"),
                    engines=first_stage_data.get("engines"),
                    fuel_amount_tons=first_stage_data.get("fuel_amount_tons"),
                    burn_time_sec=first_stage_data.get("burn_time_sec"),
                    rocket_uuid=rocket.rocket_uuid,  # One-to-one reference
                )
                session.merge(first_stage)

            # Insert SecondStage (one-to-one)
            second_stage_data = item.get("second_stage")
            if second_stage_data:
                second_stage = SecondStage(
                    reusable=second_stage_data.get("reusable"),
                    engines=second_stage_data.get("engines"),
                    fuel_amount_tons=second_stage_data.get("fuel_amount_tons"),
                    rocket_uuid=rocket.rocket_uuid,  # One-to-one reference
                )
                session.merge(second_stage)

        session.commit()
        print("Rocket, FirstStage, and SecondStage data inserted successfully.")

    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")

def fetch_and_load_launches(session: Session) -> None:
    """
    Fetch launch data from SpaceX API and insert into the database.
    """
    try:
        response = requests.get(SPACEX_LAUNCHES_URL)
        response.raise_for_status()
        launches_data = response.json()

        print(f"Found {len(launches_data)} launches")

        for item in launches_data:
            # Check if the rocket exists
            rocket = session.query(Rocket).filter(Rocket.rocket_uuid == item["rocket"]).first()
            if not rocket:
                print(f"Skipping launch {item['id']} because rocket {item['rocket']} is missing")
                continue

            launch = Launch(
                launched_uuid=item["id"],
                details=item.get("details"),
                mission_name=item.get("name"),
                upcoming=item.get("upcoming"),
                success=item.get("success"),
                image=item["links"]["patch"]["small"] if item["links"]["patch"] else None,
                webcast=item["links"]["webcast"],
                article=item["links"]["article"],
                rocket_uuid=rocket.rocket_uuid,  # Many-to-One reference
            )
            session.merge(launch)

            # Insert Failures (if any)
            failure_data = item.get("failures", [])
            for failure in failure_data:
                failure_record = Failure(
                    launched_uuid=launch.launched_uuid,
                    time=failure.get("time"),
                    reason=failure.get("reason"),
                )
                session.merge(failure_record)

        session.commit()
        print("Launch data inserted successfully.")

    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")

def fetch_and_load_starlinks(session: Session) -> None:
    """
    Fetch Starlink data from SpaceX API and insert into the database.
    """
    try:
        response = requests.get(SPACEX_STARLINK_URL)
        response.raise_for_status()
        starlinks_data = response.json()

        print(f"Found {len(starlinks_data)} starlinks")

        for item in starlinks_data:
            # Handle missing launch
            launch = session.query(Launch).filter(Launch.launched_uuid == item.get("launch")).first()
            launch_uuid = launch.launched_uuid if launch else None

            starlink = Starlink(
                starlink_uuid=item["id"],
                name=item.get("spaceTrack", {}).get("OBJECT_NAME"),
                creation_date=item.get("spaceTrack", {}).get("CREATION_DATE"),
                object_name=item.get("spaceTrack", {}).get("OBJECT_NAME"),
                country_code=item.get("spaceTrack", {}).get("COUNTRY_CODE"),
                launched_uuid=launch_uuid,  # This can now be None
            )
            session.merge(starlink)

        session.commit()
        print("Starlink data inserted successfully.")

    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")
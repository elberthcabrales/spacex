# scripts/populate_rockets.py
from sqlmodel import create_engine, Session
from app.infrastructure.scripts.rocket_loader import fetch_and_load_rockets

DATABASE_URL = "postgresql+psycopg2://postgres:12341234@localhost:5432/spacex"

def main():
    engine = create_engine(DATABASE_URL, echo=True)
    with Session(engine) as session:
        fetch_and_load_rockets(session)

if __name__ == "__main__":
    main()

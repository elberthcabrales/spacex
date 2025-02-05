from sqlalchemy.orm import Session
from app.core.domain.launch import Launch
from app.core.domain.rocket import Rocket
from app.core.domain.starlink import Starlink
from app.core.domain.dashboard import DashboardStatistics, LatestLaunch

def get_dashboard_statistics(db: Session) -> DashboardStatistics:
    """Fetch SpaceX statistics for the dashboard."""
    total_launches = db.query(Launch).count()
    total_rockets = db.query(Rocket).count()
    total_starlinks = db.query(Starlink).count()
    
    successful_launches = db.query(Launch).filter(Launch.success == True).count()
    failed_launches = total_launches - successful_launches
    
    latest_launch = (
        db.query(Launch)
        .join(Rocket, Launch.rocket_uuid == Rocket.rocket_uuid)
        .order_by(Rocket.first_flight.desc())
        .first()
    )
    
    return DashboardStatistics(
        total_launches=total_launches,
        successful_launches=successful_launches,
        failed_launches=failed_launches,
        total_rockets=total_rockets,
        total_starlinks=total_starlinks,
        latest_launch=LatestLaunch(
            mission_name=latest_launch.mission_name if latest_launch else None,
            launch_date=latest_launch.rocket.first_flight if latest_launch.rocket else None,
            success=latest_launch.success if latest_launch else None
        )
    )

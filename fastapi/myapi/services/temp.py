from sqlalchemy import select, func
from geoalchemy2.shape import to_shape
from shapely.geometry import mapping

from myapi.models.link import Link
from myapi.models.speed_record import SpeedRecord
from myapi.schemas.link import LinkAggregateResponse
from myapi.routers.aggregates import PERIOD_NAME_TO_INT


async def get_slow_links_service(session, period: str, threshold: float, min_days: int):
    period_lower = period.lower()
    if period_lower not in PERIOD_NAME_TO_INT:
        raise ValueError(f"Invalid period: {period}. Must be one of ({list(PERIOD_NAME_TO_INT.keys())})")

    period_int = PERIOD_NAME_TO_INT[period_lower]

    # Efficient single query: join + group + filter
    stmt = (
        select(
            Link,
            func.count(SpeedRecord.id).label("slow_days")
        )
        .join(SpeedRecord, SpeedRecord.link_id == Link.id)
        .where(
            SpeedRecord.period == period_int,
            SpeedRecord.average_speed < threshold,
            SpeedRecord.average_speed.isnot(None)
        )
        .group_by(Link.id)
        .having(func.count(SpeedRecord.id) >= min_days)
    )

    result = await session.execute(stmt)
    rows = result.all()

    responses = []
    for link, _ in rows:
        geometry_as_shapely = to_shape(link.geometry)
        geojson_geometry = mapping(geometry_as_shapely)

        responses.append(
            LinkAggregateResponse(
                type="Feature",
                geometry=geojson_geometry,
                properties={
                    "link_id": link.id,
                    "road_name": link.road_name,
                    "usdk_speed_category": link.usdk_speed_category,
                    "funclass_id": link.funclass_id,
                    "volume_year": link.volume_year,
                    "average_speed": None,  # could add real value here if needed
                    "day": None,
                    "period": period_int,
                }
            )
        )

    return responses

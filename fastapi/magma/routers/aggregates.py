from fastapi import APIRouter, Path, HTTPException, Query
from sqlalchemy import select, func
from geoalchemy2.shape import to_shape
from magma.core.dependencies import AsyncSessionDep
from magma.models.link import Link
from magma.models.speed_record import SpeedRecord
from pydantic import BaseModel, Field
from typing import List, Optional, Tuple, Dict, Any, Literal
from shapely.geometry import mapping


# ########    FastAPI ROUTER:  aggregates    ########


router = APIRouter()

# Map day names to their integer values
DAY_NAME_TO_INT = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6,
}

# Map time period names to their integer values
PERIOD_NAME_TO_INT = {
    "overnight": 1,
    "early_morning": 2,
    "am_peak": 3,
    "midday": 4,
    "early_afternoon": 5,
    "pm_peak": 6,
    "evening": 7,
}
# Time periods - start time, end time
# 1 Overnight 00:00 03:59
# 2 Early Morning 04:00 06:59
# 3 AM Peak 07:00 09:59
# 4 Midday 10:00 12:59
# 5 Early Afternoon 13:00 15:59
# 6 PM Peak 16:00 18:59
# 7 Evening 19:00 23:59


# ########  AGGREGATE RESPONSE MODELS  -  TODO: Ideally move these to /schemas/aggregate.py if time allows.

# /aggregates?day={day}&period={period}
class AggregatedSpeedResponse(BaseModel):
    link_id: int
    average_speed: float


# /aggregates/{link_id}?day={day}&period={period}
class LinkAggregateResponse(BaseModel):
    type: Literal["Feature"] = "Feature"
    geometry: Dict[str, Any]  # Must include 'type' and 'coordinates' keys as per GeoJSON spec
    properties: Dict[str, Any]  # Contains metadata and scalar fields for this feature

    class Config:
        schema_extra = {
            "example": {
                "type": "Feature",
                "geometry": {
                    "type": "MultiLineString",
                    "coordinates": [
                        [[-121.123, 38.123], [-121.124, 38.124]]
                    ]
                },
                "properties": {
                    "link_id": 123,
                    "road_name": "Main St",
                    "average_speed": 45.0,
                    "usdk_speed_category": 2,
                    "funclass_id": 3,
                    "volume_year": 2023,
                    "day": 2,
                    "period": 3
                }
            }
        }


# ########  UTILITY FUNCTIONS - Parameter validation and conversion.  Link ID validation and Link retrieval.

def day_to_int(day) -> int:
    day = day.lower()
    if day not in DAY_NAME_TO_INT:
        raise HTTPException(status_code=400,
            detail=f"Invalid day: {day}. Must be one of {list(DAY_NAME_TO_INT.keys())}")
    return DAY_NAME_TO_INT[day]


def period_to_int(period) -> int:
    period = period.lower()
    if period not in PERIOD_NAME_TO_INT:
        raise HTTPException(status_code=400,
            detail=f"Invalid period: {period}. Must be one of {list(PERIOD_NAME_TO_INT.keys())}")
    return PERIOD_NAME_TO_INT[period]


async def validate_link_id_and_get_link(session, link_id) -> Link:
    validate_link_statement = select(Link).where(Link.id == link_id)
    link_result = await session.execute(validate_link_statement)
    link = link_result.scalar_one_or_none()
    if not link:
        raise HTTPException(status_code=404, detail=f"Invalid Link ID: {link_id}. Not found.")
    return link


# --------  AGGREGATES BY DAY, PERIOD  --------------------------------
# SPECIFICATION:  "Aggregated average speed per link for the given day and time period."  -  STRATEGY:
# 1. For each link_id, collect/group all SpeedRecords for that link_id, for a given day and time period.
# 2. Compute the average of the 'average_speed' column for each group of SpeedRecords for each link_id.
# 3. Return a list of pairs of each link_id with it's computed average of the average_speeds for that day/period.
# * Input conversion required (names to ints)
@router.get("/aggregated_speeds/", response_model=List[AggregatedSpeedResponse])
async def get_aggregated_speeds(
        session: AsyncSessionDep,
        day: str = Query(...,
            description=f"Day of week ({list(DAY_NAME_TO_INT.keys())})"),
        period: str = Query(...,
            description=f"Time period ({list(PERIOD_NAME_TO_INT.keys())})"),
    ):
    """
    Returns aggregated average speed per link for the given day and time period.
    """

    period = period.replace(" ", "_")  # period handles spaces
    day_int = day_to_int(day)
    period_int = period_to_int(period)

    statement = (
        select(
            SpeedRecord.link_id,
            func.avg(SpeedRecord.average_speed).label("average_speed")
        )
        .where(
            SpeedRecord.day_of_week == day_int,
            SpeedRecord.period == period_int,
            SpeedRecord.average_speed.isnot(None)
        )
        .group_by(SpeedRecord.link_id)
    )
    result = await session.execute(statement)
    rows = result.all()
    return [AggregatedSpeedResponse(link_id=row.link_id, average_speed=row.average_speed) for row in rows]


# --------  FOR A LINK_ID, AGGREGATED SPEED & META DATA BY DAY, PERIOD  --------------------------------
# SPECIFICATION:  "Speed and metadata for a single road segment."  -  STRATEGY:
# 1. For a single link_id. collect all SpeedRecords for a given day and time period.
# 2. Compute the average of the 'average_speed' column. Return that along with that link_id's meta data as well.
@router.get("/aggregates/{link_id}", response_model=LinkAggregateResponse)
async def get_link_aggregate(
        session: AsyncSessionDep,
        link_id: int = Path(..., description="ID of the link"),
        day: str = Query(...,
            description=f"Day of week ({list(DAY_NAME_TO_INT.keys())})"),
        period: str = Query(...,
            description=f"Time period ({list(PERIOD_NAME_TO_INT.keys())})"),
    ):
    """
    Returns speed and metadata for a single road segment (link_id) for a given day and time period.
    """

    day_int = day_to_int(day)
    period_int = period_to_int(period)

    valid_link_record = await validate_link_id_and_get_link(session, link_id)

    statement = (
        select(func.avg(SpeedRecord.average_speed).label("average_speed"))
        .where(
            SpeedRecord.link_id == link_id,
            SpeedRecord.day_of_week == day_int,
            SpeedRecord.period == period_int,
            SpeedRecord.average_speed.isnot(None),
        )
    )
    speed_result = await session.execute(statement)
    avg_speed = speed_result.scalar()

    geometry_as_shapely = to_shape(valid_link_record.geometry)
    geojson_geometry = mapping(geometry_as_shapely)

    return LinkAggregateResponse(
        type="Feature",
        geometry=geojson_geometry,
        properties={
            "link_id": valid_link_record.id,
            "road_name": valid_link_record.road_name,
            "usdk_speed_category": valid_link_record.usdk_speed_category,
            "funclass_id": valid_link_record.funclass_id,
            "volume_year": valid_link_record.volume_year,
            "average_speed": avg_speed,
            "day": day_int,
            "period": period_int,
        }
    )


# TODO: Re-write this. Specs for # 1. for "Aggregated average speed per link for the given day and time period."
#    change a little when you look at the description for MapBox visualization. The output needs to be a list
#    of the full GeoJSON Features, etc. The spec doc leaves it a little ambiguous.
# --------  TODO: MODIFY THIS: FOR ALL LINK_IDS, AGGREGATED SPEED & META DATA BY DAY, PERIOD  --------------------------------
# SPECIFICATION:  "Speed and metadata for a single road segment."  -  STRATEGY:
# 1. For a single link_id. collect all SpeedRecords for a given day and time period.
# 2. Compute the average of the 'average_speed' column. Return that along with that link_id's meta data as well.
@router.get("/aggregates", response_model=List[LinkAggregateResponse])
async def get_link_aggregates(
        session: AsyncSessionDep,
        day: str = Query(...,
            description=f"Day of week ({list(DAY_NAME_TO_INT.keys())})"),
        period: str = Query(...,
            description=f"Time period ({list(PERIOD_NAME_TO_INT.keys())})"),
    ):
    """
    Returns speed and metadata for all road segments (link_ids) for a given day and time period. (MapBox GeoJSON format)
    """

    day_int = day_to_int(day)
    period_int = period_to_int(period)

    # Single query: Join Link and SpeedRecord, group by link_id
    statement = (
        select(
            Link,
            func.avg(SpeedRecord.average_speed).label("average_speed")
        )
        .join(SpeedRecord, SpeedRecord.link_id == Link.id)
        .where(
            SpeedRecord.day_of_week == day_int,
            SpeedRecord.period == period_int,
            SpeedRecord.average_speed.isnot(None),
        )
        .group_by(Link.id)
    )

    result = await session.execute(statement)
    rows = result.all()

    responses = []
    for link, avg_speed in rows:
        geometry_as_shapely = to_shape(link.geometry)
        geojson_geometry = mapping(geometry_as_shapely)

        responses.append(LinkAggregateResponse(
            type="Feature",
            geometry=geojson_geometry,
            properties={
                "link_id": link.id,
                "road_name": link.road_name,
                "usdk_speed_category": link.usdk_speed_category,
                "funclass_id": link.funclass_id,
                "volume_year": link.volume_year,
                "average_speed": avg_speed,
                "day": day_int,
                "period": period_int,
            }
        ))

    return responses


# Queries for which we have good data:
# http://localhost:48000/aggregates/?day=wednesday&period=am_peak


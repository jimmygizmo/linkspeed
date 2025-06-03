from fastapi import APIRouter, Path, HTTPException, Query
from sqlalchemy import select, func
# from sqlalchemy.ext.asyncio import AsyncSession
from magma.core.dependencies import AsyncSessionDep
from magma.models.link import Link
from magma.models.speed_record import SpeedRecord
from pydantic import BaseModel
from typing import List, Optional


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


# ########  AGGREGATE RESPONSE MODELS  -  TODO: Ideally move these to /schemas/aggregate.py if time allows.

# /aggregates?day={day}&period={period}
class AggregatedSpeedResponse(BaseModel):
    link_id: int
    average_speed: float


# /aggregates/{link_id}?day={day}&period={period}
class LinkAggregateResponse(BaseModel):
    link_id: int
    road_name: Optional[str]
    funclass_id: Optional[int]
    average_speed: Optional[float]
    period: int
    day: int


# --------  AGGREGATES BY DAY, PERIOD  --------------------------------
# SPECIFICATION:  "Aggregated average speed per link for the given day and time period."  -  STRATEGY:
# 1. For each link_id, collect/group all SpeedRecords for that link_id, for a given day and time period.
# 2. Compute the average of the 'average_speed' column for each group of SpeedRecords for each link_id.
# 3. Return a list of pairs of each link_id with it's computed average of the average_speeds for that day/period.
# * Input conversion required (names to ints)
@router.get("/aggregates/", response_model=List[AggregatedSpeedResponse])
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

    day = day.lower()
    period = period.lower()

    if day not in DAY_NAME_TO_INT:
        raise HTTPException(status_code=400,
            detail=f"Invalid day: {day}. Must be one of {list(DAY_NAME_TO_INT.keys())}")

    if period not in PERIOD_NAME_TO_INT:
        raise HTTPException(status_code=400,
            detail=f"Invalid period: {period}. Must be one of {list(PERIOD_NAME_TO_INT.keys())}")

    day_int = DAY_NAME_TO_INT[day]
    period_int = PERIOD_NAME_TO_INT[period]

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
        day: int = Query(..., ge=0, le=6, description="Day of week (0=Mon - 6=Sun)"),
        period: int = Query(..., ge=0, le=7, description="Time period of the day (1-7)"),
    ):
    """
    Returns speed and metadata for a single road segment (link_id) for a given day and time period.
    """

    validate_link_statement = select(Link).where(Link.id == link_id)
    link_result = await session.execute(validate_link_statement)
    link = link_result.scalar_one_or_none()
    if not link:
        raise HTTPException(status_code=404, detail=f"Invalid Link ID: {link_id}. Not found.")

    statement = (
        select(func.avg(SpeedRecord.average_speed).label("average_speed"))
        .where(
            SpeedRecord.link_id == link_id,
            SpeedRecord.day_of_week == day,
            SpeedRecord.period == period,
            SpeedRecord.average_speed.isnot(None)
        )
    )
    speed_result = await session.execute(statement)
    avg_speed = speed_result.scalar()
    return LinkAggregateResponse(
        link_id=link.id,
        road_name=link.road_name,
        funclass_id=link.funclass_id,
        average_speed=avg_speed,
        day=day,
        period=period
    )




# Time periods
# 1 Overnight 00:00 03:59
# 2 Early Morning 04:00 06:59
# 3 AM Peak 07:00 09:59
# 4 Midday 10:00 12:59
# 5 Early Afternoon 13:00 15:59
# 6 PM Peak 16:00 18:59
# 7 Evening 19:00 23:59

# Queries for which we have good data:
# http://localhost:48000/aggregates/?day=wednesday&period=am_peak


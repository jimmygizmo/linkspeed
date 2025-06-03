from fastapi import APIRouter, Query
from sqlalchemy import select, func
# from sqlalchemy.ext.asyncio import AsyncSession
from magma.core.dependencies import AsyncSessionDep
from magma.models.link import Link
from magma.models.speed_record import SpeedRecord
from pydantic import BaseModel
from typing import List


router = APIRouter()


# Response model
class AggregatedSpeedResponse(BaseModel):
    link_id: int
    average_speed: float

# Time periods
# 1 Overnight 00:00 03:59
# 2 Early Morning 04:00 06:59
# 3 AM Peak 07:00 09:59
# 4 Midday 10:00 12:59
# 5 Early Afternoon 13:00 15:59
# 6 PM Peak 16:00 18:59
# 7 Evening 19:00 23:59


@router.get("/aggregates/", response_model=List[AggregatedSpeedResponse])
async def get_aggregated_speeds(
    session: AsyncSessionDep,
    day: int = Query(..., ge=0, le=6, description="Day of the week (0=Monday to 6=Sunday)"),
    period: int = Query(..., ge=0, description="Time period of the day (e.g. 0=early morning, etc.)"),
):
    """
    Returns aggregated average speed per link for the given day and time period.
    """

    stmt = (
        select(
            SpeedRecord.link_id,
            func.avg(SpeedRecord.average_speed).label("average_speed")
        )
        .where(
            SpeedRecord.day_of_week == day,
            SpeedRecord.period == period,
            SpeedRecord.average_speed.isnot(None)
        )
        .group_by(SpeedRecord.link_id)
    )

    result = await session.execute(stmt)
    rows = result.all()

    return [AggregatedSpeedResponse(link_id=row.link_id, average_speed=row.average_speed) for row in rows]


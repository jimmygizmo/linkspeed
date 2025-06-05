from fastapi import APIRouter, Path, Query
from typing import List
from myapi.core.dependencies import AsyncSessionDep
from myapi.schemas.link import LinkAggregateResponse
from myapi.services.aggregates import get_single_link_aggregate, get_all_link_aggregates


# ########    FastAPI ROUTER:  aggregates    ########


# TODO: Need to consolidate these lookups to a single logical place as we use them in 2-3 different files.
DAY_NAME_TO_INT = {
    "monday": 0, "tuesday": 1, "wednesday": 2,
    "thursday": 3, "friday": 4, "saturday": 5, "sunday": 6
}
PERIOD_NAME_TO_INT = {
    "overnight": 1, "early_morning": 2, "am_peak": 3,
    "midday": 4, "early_afternoon": 5, "pm_peak": 6, "evening": 7
}

router = APIRouter()


@router.get("/aggregates/{link_id}", response_model=LinkAggregateResponse)
async def get_link_aggregate(
        session: AsyncSessionDep,
        link_id: int = Path(..., description="ID of the link"),
        day: str = Query(...,
            description=f"Day of week ({list(DAY_NAME_TO_INT.keys())})"),
        period: str = Query(...,
            description=f"Time period ({list(PERIOD_NAME_TO_INT.keys())})"),
    ):
    return await get_single_link_aggregate(session, link_id, day, period)


@router.get("/aggregates", response_model=List[LinkAggregateResponse])
async def get_link_aggregates(
        session: AsyncSessionDep,
        day: str = Query(...,
            description=f"Day of week ({list(DAY_NAME_TO_INT.keys())})"),
        period: str = Query(...,
            description=f"Time period ({list(PERIOD_NAME_TO_INT.keys())})"),
    ):
    return await get_all_link_aggregates(session, day, period)


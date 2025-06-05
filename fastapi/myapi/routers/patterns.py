from fastapi import APIRouter, Query, HTTPException
from myapi.core.dependencies import AsyncSessionDep
from typing import List
from myapi.schemas.link import LinkAggregateResponse
from myapi.services.patterns import get_slow_links_service


# ########    FastAPI ROUTER:  patterns    ########


# TODO: Need to consolidate these lookups to a single logical place as we use them in 2-3 different files.
PERIOD_NAME_TO_INT = {
    "overnight": 1, "early_morning": 2, "am_peak": 3,
    "midday": 4, "early_afternoon": 5, "pm_peak": 6, "evening": 7
}

router = APIRouter()


@router.get("/patterns/slow_links", response_model=List[LinkAggregateResponse])
async def get_slow_links(
        session: AsyncSessionDep,
        period: str = Query(...,
            description=f"Time period ({list(PERIOD_NAME_TO_INT.keys())})"),
        threshold: float = Query(..., description="Speed threshold in mph"),
        min_days: int = Query(..., description="Minimum number of days with slow speeds"),
    ):
    """
    Returns links that have average speeds below the given threshold for at least `min_days` in the same period.
    """
    try:
        return await get_slow_links_service(session, period, threshold, min_days)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))


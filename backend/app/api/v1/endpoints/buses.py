from typing import Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.fleet import Bus
from app.schemas.fleet import BusResponse

router = APIRouter()

@router.get("/", response_model=List[BusResponse])
async def read_buses(
    db: AsyncSession = Depends(get_db),
    current_user: Any = Depends(get_current_user), # Any authenticated user can view buses for now
) -> Any:
    """
    Retrieve all buses in the fleet.
    """
    result = await db.execute(select(Bus))
    buses = result.scalars().all()
    return buses

from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.session import get_session

router = APIRouter()


@router.get("/")
async def health_check(
    response: Response, session: Annotated[AsyncSession, Depends(get_session)]
) -> dict[str, str]:
    try:
        await session.exec(select(1))
        db_status = "up"
        return {"status": "ok", "database": db_status}
    except Exception:
        db_status = "down"
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "error", "database": db_status}

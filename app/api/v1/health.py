from fastapi import APIRouter, Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.session import get_session

router = APIRouter()


@router.get("/")
async def health_check(session: AsyncSession = Depends(get_session)):
    try:
        await session.exec(select(1))
        db_status = "up"
    except Exception:
        db_status = "down"
    return {"status": "ok", "database": db_status}

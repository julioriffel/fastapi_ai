from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.session import get_session
from app.models.user import User, UserCreate
from app.crud.user import user_crud

from app.api.deps import CurrentUser

router = APIRouter()


@router.get("/me", response_model=User)
async def read_user_me(
    current_user: CurrentUser,
) -> Any:
    """
    Get current user.
    """
    return current_user


@router.get("/", response_model=List[User])
async def read_users(
    session: AsyncSession = Depends(get_session),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve users.
    """
    return await user_crud.get_multi(session, skip=skip, limit=limit)


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(
    *,
    session: AsyncSession = Depends(get_session),
    user_in: UserCreate,
) -> Any:
    """
    Create new user.
    """
    user = await user_crud.get_by_email(session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    return await user_crud.create(session, obj_in=user_in)

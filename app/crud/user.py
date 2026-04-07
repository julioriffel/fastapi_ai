from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.security import get_password_hash
from app.models.user import User, UserCreate


class CRUDUser:
    async def get_by_email(self, db: AsyncSession, *, email: str) -> User | None:
        statement = select(User).where(User.email == email)
        result = await db.exec(statement)
        return result.first()

    async def get_by_id(self, db: AsyncSession, *, id: int) -> User | None:
        statement = select(User).where(User.id == id)
        result = await db.exec(statement)
        return result.first()

    async def authenticate(
        self, db: AsyncSession, *, email: str, password: str
    ) -> User | None:
        user = await self.get_by_email(db, email=email)
        if not user:
            return None
        from app.core.security import verify_password

        if not verify_password(password, user.hashed_password):
            return None
        return user

    async def get_multi(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> list[User]:
        statement = select(User).offset(skip).limit(limit)
        result = await db.exec(statement)
        return list(result.all())

    async def create(self, db: AsyncSession, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            is_active=obj_in.is_active,
            is_superuser=obj_in.is_superuser,
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


user_crud = CRUDUser()

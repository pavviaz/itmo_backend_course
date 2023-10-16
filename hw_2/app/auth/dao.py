import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import User


async def get_user(session: AsyncSession, username: str) -> User | None:
    q = sa.select(User).where(User.username == username)
    user = await session.execute(q)

    return user.scalar_one_or_none()


async def add_user(session: AsyncSession, **user_data):
    q = sa.insert(User).values(**user_data)
    await session.execute(q)
    await session.commit()

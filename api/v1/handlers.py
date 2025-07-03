from typing import Sequence, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select, insert

from api.v1.models import CreateUser, UpdateUser
from db.models import User


async def get_all_users(session: AsyncSession) -> Sequence[User]:
    """Select all users."""

    stmt = select(User)
    result = await session.execute(stmt)

    return result.scalars().all()


async def get_user_by_email(session: AsyncSession, email: str) -> User:
    """Select user by email."""

    stmt = select(User).where(User.email == email)
    result = await session.execute(stmt)

    return result.scalars().first()


async def post_new_user(session: AsyncSession, user: CreateUser) -> bool:
    """Create new user."""

    stmt = insert(User).values(user.dict())
    result = await session.execute(stmt)
    await session.commit()

    if result:
        return True

    return False


async def update_user_data(
        session: AsyncSession,
        email: str,
        user_data: UpdateUser
) -> Optional[User]:
    """Update user data."""
    user = await get_user_by_email(session, email)
    if not user:
        return None

    update_data = user_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)

    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user





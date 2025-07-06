from typing import Sequence, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select, and_

from api.v1.models import UserCreate, UserUpdate
from core.security import get_password_hash
from db.models import User


async def get_all_users(
        session: AsyncSession,
        gender: Optional[bool] = None,
        min_age: Optional[int] = None,
        max_age: Optional[int] = None
        ) -> Sequence[User]:
            """Select all users."""
            conditions = []

            stmt = select(User)

            if gender is not None:
                conditions.append(User.gender == gender)

            if min_age:
                conditions.append(User.age >= min_age)

            if max_age:
                conditions.append(User.age <= max_age)

            if conditions:
                    stmt = stmt.where(and_(*conditions))

            result = await session.execute(stmt)

            return result.scalars().all()


async def get_user_by_email(session: AsyncSession, email: str) -> User:
    """Select user by email."""

    stmt = select(User).where(User.email == email)
    result = await session.execute(stmt)

    return result.scalars().first()


async def post_new_user(session: AsyncSession, user: UserCreate) -> bool:
    """Create new user."""

    user_data = user.dict(exclude={"password"})
    user_data["hashed_password"] = get_password_hash(user.password.get_secret_value())
    user_data.update({
        "is_superuser": False,
        "is_active": True
    })
    db_user = User(**user_data)

    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    return db_user


async def update_user_data(
        session: AsyncSession,
        email: str,
        user: UserUpdate
) -> Optional[User]:
    """Update user data."""
    user_data = user.dict(exclude={"password"})
    user_data["hashed_password"] = get_password_hash(user.password.get_secret_value())
    user = await get_user_by_email(session, email)
    if not user:
        return None

    for key, value in user_data.items():
        setattr(user, key, value)

    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def delete_user_by_email(
        session: AsyncSession,
        email: str
) -> bool:
    """Delete user by email."""
    user = await get_user_by_email(session, email)
    if not user:
        return False

    await session.delete(user)
    await session.commit()
    return True

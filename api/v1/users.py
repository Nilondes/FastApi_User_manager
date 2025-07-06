from http import HTTPStatus
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.dependencies import get_current_superuser, get_current_active_user
from api.v1.handlers import get_all_users, get_user_by_email, post_new_user, update_user_data, delete_user_by_email
from api.v1.models import UserCreate, UserInDB, UserUpdate, UserSelfUpdate
from db.connectors import get_db_session
from db.models import User

router = APIRouter()


@router.get("", response_model=List[UserInDB], dependencies=[Depends(get_current_superuser)])
async def get_users(
        session: AsyncSession = Depends(get_db_session),
        gender: Optional[bool] = Query(
            None,
            description="Filter by gender (false for male, true for female)"),
        min_age: Optional[int] = Query(
            None,
            description="Minimum age (inclusive)"),
        max_age: Optional[int] = Query(
            None,
            description="Maximum age (inclusive)")
        ):
        users = await get_all_users(
            session,
            gender=gender,
            min_age=min_age,
            max_age=max_age
        )

        if not users:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                                detail="No users found")

        return users


@router.get("/me", response_model=UserInDB)
async def get_my_profile(
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_db_session)
):
    """Get current user's profile"""

    return current_user


@router.patch("/me", response_model=UserInDB)
async def update_my_profile(
        user_data: UserSelfUpdate,
        current_user: User = Depends(get_current_active_user),
        session: AsyncSession = Depends(get_db_session),
):
    allowed_fields = ["name", "password", "gender", "age"]
    update_data = {k: v for k, v in user_data.dict().items()
                   if k in allowed_fields and v is not None}

    return await update_user_data(session, current_user.email, UserSelfUpdate(**update_data))


@router.get("/{email}", response_model=UserInDB, dependencies=[Depends(get_current_superuser)])
async def get_user(email: str,
                   session: AsyncSession = Depends(get_db_session)):

    user = await get_user_by_email(session, email=email)

    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="No user found")

    return user


@router.post("", response_model=UserInDB, dependencies=[Depends(get_current_superuser)])
async def add_user(user: UserCreate, session: AsyncSession = Depends(get_db_session)):
    existing_user = await get_user_by_email(session, user.email)
    if existing_user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="User with this email already exists"
        )

    new_user = await post_new_user(session, user=user)


    if not new_user:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                            detail="No user created")

    return new_user


@router.patch("/{email}", response_model=UserInDB, dependencies=[Depends(get_current_superuser)])
async def update_user(
    email: str,
    user_data: UserUpdate,
    session: AsyncSession = Depends(get_db_session),
):

    updated_user = await update_user_data(session, email, user_data)
    if not updated_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="User not found"
        )
    return updated_user


@router.delete("/{email}",
               dependencies=[Depends(get_current_superuser)])
async def delete_user(
    email: str,
    session: AsyncSession = Depends(get_db_session),
):
    """Delete a user by email (admin only)."""
    deleted = await delete_user_by_email(session, email)
    if not deleted:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="User not found"
        )

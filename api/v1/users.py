from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.dependencies import get_current_superuser
from api.v1.handlers import get_all_users, get_user_by_email, post_new_user, update_user_data
from api.v1.models import UserCreate, UserInDB, UserUpdate
from db.connectors import get_db_session

router = APIRouter()


@router.get("", response_model=List[UserInDB], dependencies=[Depends(get_current_superuser)])
async def get_users(session: AsyncSession = Depends(get_db_session)):

    users = await get_all_users(session)

    if not users:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="No users found")

    return users


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

from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request

from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.handlers import get_all_users, get_user_by_email, post_new_user, update_user_data
from api.v1.models import CreateUser, User, UpdateUser
from db.connectors import get_db_session

router = APIRouter()


@router.get("", response_model=List[User])
async def get_users(request: Request, session: AsyncSession = Depends(get_db_session)):
    if not request.session.get("is_superuser"):
        raise HTTPException(status_code=403, detail="Forbidden")

    users = await get_all_users(session)

    if not users:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="No users found")

    return users


@router.get("/{email}", response_model=User)
async def get_user(request: Request, email: str,
                   session: AsyncSession = Depends(get_db_session)):
    if not request.session.get("is_superuser"):
        raise HTTPException(status_code=403, detail="Forbidden")
    user = await get_user_by_email(session, email=email)

    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="No user found")

    return user


@router.post("", response_model=User)
async def add_user(request: Request, user: CreateUser,
                   session: AsyncSession = Depends(get_db_session)):
    if not request.session.get("is_superuser"):
        raise HTTPException(status_code=403, detail="Forbidden")
    success = await post_new_user(session, user=user)

    if not success:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST,
                            detail="No user created")

    return user


@router.patch("/{email}", response_model=User)
async def update_user(
    request: Request,
    email: str,
    user_data: UpdateUser,
    session: AsyncSession = Depends(get_db_session),
):
    if not request.session.get("is_superuser"):
        raise HTTPException(status_code=403, detail="Forbidden")
    updated_user = await update_user_data(session, email, user_data)
    if not updated_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="User not found"
        )
    return updated_user

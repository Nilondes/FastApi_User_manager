from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import decode_token
from db.connectors import get_db_session
from api.v1.handlers import get_user_by_email
from db.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        session: AsyncSession = Depends(get_db_session)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_token(token)
    if not payload:
        raise credentials_exception

    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception

    user = await get_user_by_email(session, email=email)
    if user is None:
        raise credentials_exception

    return user


async def get_current_superuser(current_user: User = Depends(get_current_user)):
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="Forbidden: Superuser required"
        )
    return current_user

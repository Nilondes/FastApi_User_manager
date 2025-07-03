import uvicorn
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from api.v1.auth import router as auth_router
from api.v1.users import router as users_router


app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key="secret_key",
    session_cookie="session_cookie",
    max_age=3600
)


app.include_router(
    users_router,
    prefix="/api/v1/users",
    tags=["users"]
)

app.include_router(
    auth_router,
    prefix="/api/v1/auth",
    tags=["auth"]
)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

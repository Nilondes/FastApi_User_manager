 FastApi_User_manager

This FastAPI app allows management of users (create, edit, view, delete, block).

It also allows viewing of user list with different filters.

There are 2 roles: administrator, user.

The access to any user's CRUD is available only for administrator.

- **Backend**: Python 3.11, FastAPI
- **DB**: PostgreSQL 15, SQLAlchemy 2.0
- **Auth**: JWT, bcrypt
- **Testing**: Postman
- **Deploy**: Docker, Docker Compose 

## Available endpoints:

POST /api/v1/auth - to get access token

{

  "username": "string",
  
  "password": "string"
  
}

Superuser endpoints (is_superuser=true):

GET /api/v1/users/ - returns the list of users.

Supports the following params (search filters):

"min_age" = int,

"max_age" = int,

"gender" = bool

POST /api/v1/users/ - create new user ("is_active" = true, "is_superuser"=false)

{

  "email" = EmailStr,
  
  "username" = str,
  
  "password" = str,
  
  "age" = int,
  
  "gender" = bool
  
}

GET /api/v1/users/{email} - get user info by email

PATCH /api/v1/users/{email} - Update user info by emailm including block and grant superuser access.

{

  "username" = str,
  
  "password" = str,
  
  "age" = int,
  
  "gender" = bool,
  
  "is_active" = bool,
  
  "is_superuser" = bool
  
}

DELETE /api/v1/users/{email} - remove user.

User endpoints:

GET /api/v1/users/me - get user info

PATCH /api/v1/users/me - update user info

{

  "username" = str,
  
  "password" = str,
  
  "age" = int,
  
  "gender" = bool,
  
}


## Getting started

```sh
git clone https://github.com/Nilondes/fastapi_user_manager.git
cd fastapi_user_manager
```

The root directory should contain ".env.dev.JWT" file with the content:

JWT_SECRET=<your_secret_string>

To create db and add superuser with password="1234":

```sh
CREATE DATABASE user_manager;
INSERT INTO "user" (
    id, 
    name, 
    email, 
    gender, 
    age, 
    is_superuser, 
    is_active, 
    hashed_password
)
VALUES (
    '633539fa-dfea-4ff3-a920-725890975ca0',
    'Admin', 
    'admin@example.com', 
    true, 
    30, 
    true, 
    true, 
    '$2b$12$UYmycvUR2oyUEBpanE4rMuRxlwrO2MaMzvYh6O9Q6vXSEdtgjzby.'
);
```

To install all dependencies:

```sh
pip install -r requirements.txt
```

To start Docker from main directory:

```sh
docker compose -f docker_compose_dev.yaml --env-file .env.dev.pg up -d

```

To make migrations:

```sh
alembic upgrade head

```

To start app:

```sh
python3 main.py

```

SWAGGER is available by /docs#

Use postman file is provided to test endpoints.

The variables are:

{

  "base_url": "http://localhost:8000",
  
  "admin_email": "admin@example.com",
  
  "admin_password": "1234",
  
  "test_user_email": "test_user@example.com",
  
  "test_user_password": "test_password",
  
  "test_user1_email": "test_use1r@example.com",
  
  "test_user2_email": "test_user2@example.com",
  
  "test_user3_email": "test_user3@example.com",
  
  "test_user4_email": "test_user4@example.com"
  
}
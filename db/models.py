import uuid

from sqlalchemy import Boolean, Column, String, UUID, Integer
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    email = Column(String(320), unique=True, index=True, nullable=False)
    gender = Column(Boolean(), nullable=False)
    age = Column(Integer(), nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False, nullable=False)

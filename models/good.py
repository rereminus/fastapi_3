from typing import Union
from typing_extensions import Annotated
from sqlalchemy import Column, String, Integer, Identity
from sqlalchemy.orm import declarative_base
from enum import Enum
from pydantic import BaseModel, Field

Base = declarative_base()
userDict = {}


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, Identity(start=10), primary_key=True)
    name = Column(String, index=True, nullable=False)
    hashed_password = Column(String)


class Main_User(BaseModel):
    id: Annotated[Union[int, None], Field(default=100, ge=1, lt=200)] = None
    name: Union[str, None] = None


class Main_UserDB(Main_User):
    hashed_password: Annotated[Union[str, None], Field(max_length=200, min_length=6)] = None


class Tags(Enum):
    users = "users"
    info = "info"


class New_Response(BaseModel):
    message: str


def find_user(id: str) -> Union[User, None]:
    if userDict.get(id):
        return userDict[id]
    else:
        return None

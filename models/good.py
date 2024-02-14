from typing import Union, Annotated
from sqlalchemy import Column, String, Integer, Identity, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from enum import Enum
from pydantic import BaseModel, Field

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, Identity(start=10), primary_key=True)
    name = Column(String, index=True, nullable=False)
    hashed_password = Column(String)
    department_id = Column(Integer, ForeignKey('department.id'))
    user_dep = relationship('Department', back_populates='employees')


class Department(Base):
    __tablename__ = "department"
    id = Column(Integer, primary_key=True, autoincrement=True)
    department_name = Column(String, nullable=False)
    employees = relationship('User', back_populates='user_dep')


class Main_User(BaseModel):
    id: Annotated[Union[int, None], Field(default=100, ge=1, lt=200)] = None
    name: Union[str, None] = None
    department_id: Annotated[Union[int, None], Field(default=100, ge=1, lt=200)] = None


class Main_UserDB(Main_User):
    hashed_password: Annotated[Union[str, None], Field(max_length=200, min_length=6)] = None


class Main_Departments(BaseModel):
    id: Annotated[Union[int, None], Field(default=100, ge=1, lt=200)] = None
    department_name: Union[str, None] = None


class Tags(Enum):
    users = "users"
    info = "info"
    departments = "departments"


class New_Response(BaseModel):
    message: str

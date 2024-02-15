from sqlalchemy.orm import Session
from public.db import engine_s
from fastapi import APIRouter, Depends, Body, HTTPException
from fastapi.responses import JSONResponse
from models.good import *
from starlette import status
from typing import Annotated, Union


def get_session():
    with Session(engine_s) as session:
        try:
            yield session
        finally:
            session.close()


user_router = APIRouter(tags=[Tags.users], prefix='/api/users')


def coder_passwd(cod: str):
    return cod*2


@user_router.get("/{id}", response_model=Union[Main_User, New_Response], tags=[Tags.info])
def get_user(id: int, DB: Session = Depends(get_session)):
    user = DB.query(User).filter(User.id == id).first()
    if user is None:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
    return user


@user_router.get("/", response_model=Union[list[Main_User], New_Response], tags=[Tags.users])
def get_user_db(DB: Session = Depends(get_session)):
    users = DB.query(User).all()
    if users is None:
        return JSONResponse(status_code=404, content={"message": "Пользователи не найдены"})
    return users


@user_router.post("/", response_model=Union[Main_User, New_Response],
                  tags=[Tags.users], status_code=status.HTTP_201_CREATED)
def create_user(item: Annotated[Main_User, Body(embed=True, description="Новый пользователь")],
                DB: Session = Depends(get_session)):
    try:
        user = User(name=item.name, hashed_password=coder_passwd(item.name))
        user.department_id = item.department_id
        if user is None:
            raise HTTPException(status_code=404, detail="Объект не определен")
        DB.add(user)
        DB.commit()
        DB.refresh(user)
        return user
    except Exception:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка при добавлении объекта {user}")


@user_router.put("/", response_model=Union[Main_User, New_Response], tags=[Tags.users])
def edit_user(item: Annotated[Main_User, Body(embed=True, description="Изменение данных для пользователя по id")],
              DB: Session = Depends(get_session)):
    user = DB.query(User).filter(User.id == item.id).first()
    if user is None:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
    user.name = item.name
    user.department_id = item.department_id
    try:
        DB.commit()
        DB.refresh(user)
    except HTTPException:
        return JSONResponse(status_code=404, content={"message": "Ошибка"})
    return user

@user_router.delete("/{id}", response_model=Union[Main_User, New_Response], tags=[Tags.users])
def delete_user(id: int, DB: Session = Depends(get_session)):
    user = DB.query(User).filter(User.id == id).first()
    if user is None:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
    try:
        DB.delete(user)
        DB.commit()
    except HTTPException:
        JSONResponse(content={"message": "Ошибка"})
    return JSONResponse(content={'message': f'Пользователь удален {id}'})


@user_router.patch("/{id}", response_model=Union[Main_User, New_Response], tags=[Tags.users])
def edit_user(id: int, item: Annotated[Main_User, Body(embed=True, description="Изменение данных для пользователя по id")],
              DB: Session = Depends(get_session)):
    db_user = DB.get(User, id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    user_data = item.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)
    DB.add(db_user)
    DB.commit()
    DB.refresh(db_user)
    return db_user

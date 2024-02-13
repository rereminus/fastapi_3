from sqlalchemy.orm import Session
from public.db import engine_s
from fastapi import APIRouter, Depends, Body, HTTPException
from fastapi.responses import JSONResponse
from models.good import *
from starlette import status


def get_session():
    with Session(engine_s) as session:
        try:
            yield session
        finally:
            session.close()


user_router = APIRouter(tags=[Tags.users], prefix='/api/users')
info_router = APIRouter(tags=[Tags.info])


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
def edit_user(item: Annotated[Main_User, Body(embed=True, description="Изменяем данные по id")],
              DB: Session = Depends(get_session)):
    try:
        user = find_user(str(item.id))
        if user is None:
            return New_Response(message="Пользователь не найден")
        update_user_dict = item.model_dump(exclude_unset=True)
        for key, value in update_user_dict:
            setattr(user, key, value)
        DB.add(user)
        DB.commit()
        DB.refresh(user)
        return user
    except HTTPException:
        return JSONResponse(status_code=404, content={"message": "Ошибка"})

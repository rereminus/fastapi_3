from sqlalchemy.orm import Session
from public.db import engine_s
from fastapi import APIRouter, Depends, Body, HTTPException
from fastapi.responses import JSONResponse
from models.good import *
from starlette import status

deps_router = APIRouter(tags=[Tags.departments], prefix='/api/departments')

def get_session():
    with Session(engine_s) as session:
        try:
            yield session
        finally:
            session.close()


@deps_router.get("/", response_model=Union[list[Main_Departments], New_Response], tags=[Tags.departments])
def get_all_deps(DB: Session = Depends(get_session)):
    deps = DB.query(Department).all()
    if not deps:
        return JSONResponse(status_code=404, content={"message": "Отделы не найдены"})
    return deps


@deps_router.get("/{id}", response_model=Union[Main_Departments, New_Response], tags=[Tags.departments])
def get_dep(id: int, DB: Session = Depends(get_session)):
    dep = DB.query(Department).filter(Department.id == id).first()
    if dep is None:
        return JSONResponse(status_code=404, content={"message": "Отдел не найден"})
    return dep


@deps_router.post("/", response_model=Union[Main_Departments, New_Response],
                  tags=[Tags.departments], status_code=status.HTTP_201_CREATED)
def create_dep(item: Annotated[Main_Departments, Body(embed=True, description="Новый отдел")],
                DB: Session = Depends(get_session)):
    try:
        dep = Department(department_name=item.department_name)
        if dep is None:
            raise HTTPException(status_code=404, detail="Объект не определен")
        DB.add(dep)
        DB.commit()
        DB.refresh(dep)
        return dep
    except Exception:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка при добавлении объекта {dep}")


@deps_router.delete("/{id}", response_model=Union[Main_Departments, New_Response], tags=[Tags.departments])
def delete_dep(id: int, DB: Session = Depends(get_session)):
    dep = DB.query(Department).filter(Department.id == id).first()
    if dep is None:
        return JSONResponse(status_code=404, content={"message": "Отдел не найден"})
    try:
        DB.delete(dep)
        DB.commit()
    except HTTPException:
        JSONResponse(content={"message": "Ошибка"})
    return JSONResponse(content={'message': f'Отдел удален {id}'})

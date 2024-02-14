from sqlalchemy import create_engine, text
from sqlalchemy import insert, select
from models.good import Base, User, Department
from config import settings

ur_s = settings.POSTGRES_DATABASE_URLS
engine_s = create_engine(ur_s, echo=True)


def create_tables():
    Base.metadata.drop_all(bind=engine_s)
    Base.metadata.create_all(bind=engine_s)


def f_builder():
    with engine_s.connect() as conn:
        query_dep = select(Department.id, Department.department_name)
        ids_dep = conn.execute(query_dep).fetchall()

        query = insert(User).values([
            {"name": "Petrov", "hashed_password": "11111", "department_id": ids_dep[0][0]},
            {"name": "Sokolov", "hashed_password": "22222", "department_id": ids_dep[1][0]}
        ])
        conn.execute(query)
        conn.execute(text('commit;'))
        query = select(User)
        answer = conn.execute(query)
        print(f"answer = {answer.all()}")

def f_builder2():
    with engine_s.connect() as conn:
        query = insert(Department).values([
            {"department_name": "Бухгалтерия"},
            {"department_name": "Тех. поддержка"}
        ])
        conn.execute(query)
        conn.execute(text('commit;'))
        query = select(Department)
        answer = conn.execute(query)
        print(f"answer = {answer.all()}")

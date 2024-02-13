import databases
import sqlalchemy
import uvicorn
from datetime import datetime
from fastapi import FastAPI
from starlette.responses import PlainTextResponse
from public.router_users import user_router


DATABASE_URL = 'sqlite:///test.db'
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)

app = FastAPI()
#asyncio.run(f_builder())
#create_tables()


app.include_router(user_router)
@app.on_event("startup")
def on_startup():
    open("log_p.txt", mode="a").write(f'{datetime.utcnow()}: Begin\n')
@app.on_event("shutdown")
def shutdown():
    open("log_p.txt", mode="a").write(f'{datetime.utcnow()}: End\n')
@app.get('/', response_class=PlainTextResponse)
def f_indexH():
    return "Начальная страница"

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
from fastapi import FastAPI, Response, Path, Query, Body, Header
from fastapi.responses import HTMLResponse, PlainTextResponse, JSONResponse, FileResponse
from public.users import users_router

app = FastAPI()

app.include_router(users_router)

@app.get('/', response_class=PlainTextResponse)
def f_indexH():
    return "Начальная страница"
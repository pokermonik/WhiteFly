from fastapi import FastAPI, Form, Request, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import time

from shared.database import init_db, save_to_db

app = FastAPI()
init_db()
templates = Jinja2Templates(directory="src/zad2/templates")


@app.get("/sync", response_class=HTMLResponse)
async def get_sync_form(request: Request):
    
    return templates.TemplateResponse(
        request=request, 
        name="fast_sync.html", 
        context={"request": request}
    )   

@app.post("/sync")
async def post_sync_form(name: str = Form(...), surname: str = Form(...)):
    save_to_db(name, surname)
    print(f"Zapisano synchronicznie do bazy: {name} {surname}")
    return {"status": "success", "message": "Dane zapisane synchronicznie"}

@app.get("/async", response_class=HTMLResponse)
async def get_async_form(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="fast_async.html", 
        context={"request": request}
    )

def heavy_background_task(name: str, surname: str):
    """Funkcja wykonywana w tle po odesłaniu odpowiedzi do klienta"""
    time.sleep(5)
    save_to_db(name, surname)
    print(f"Zadanie w tle zakończone dla: {name} {surname}")

@app.post("/async")
async def post_async_form(background_tasks: BackgroundTasks, name: str = Form(...), surname: str = Form(...)):
    background_tasks.add_task(heavy_background_task, name, surname)
    return {"status": "accepted", "message": "Dane przyjęte, przetwarzanie w tle rozpoczęte"}
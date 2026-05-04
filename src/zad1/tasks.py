from celery import Celery
import time
from shared.database import save_to_db

celery_app = Celery('tasks', broker='redis://127.0.0.1:6379/0')

@celery_app.task
def process_user_task(name,surname):
    time.sleep(5) 
    save_to_db(name, surname)
    print(f"[WORKER] Zapisano do bazy: {name} {surname}")
    
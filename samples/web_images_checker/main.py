
from fastapi import FastAPI
from celery.result import AsyncResult

from worker import tasks
from worker.celery_handler import celery_app

app = FastAPI()


@app.post("/image/analyze")
def image_analyze(image_url: str) -> dict:
    task = tasks.analyze_image.delay(image_url)
    return {
        "task_id": task.id,
        "status_url": f"/image/status/{task.id}",
    }

@app.get("/image/status/{task_id}")
def image_status(task_id: str) -> dict:
    image_task = AsyncResult(task_id, app=celery_app)

    response = {
        "task_id": task_id,
        "status": image_task.status,
    }
    if image_task.ready():
        response["result"] = image_task.result

    return response

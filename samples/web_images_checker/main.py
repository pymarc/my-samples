
from fastapi import FastAPI

app = FastAPI()


@app.post("/image/analyze")
async def image_analyze() -> dict:
    return {
        "task_id": "1234567890",
        "status": "accepted"
    }

@app.get("/image/status/{task_id}")
async def image_status(task_id: str) -> dict:
    return {
        "task_id": task_id,
        "status": "completed"
    }

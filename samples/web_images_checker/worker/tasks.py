
import time
import logging
import requests
from io import BytesIO
from PIL import Image, UnidentifiedImageError

from worker.celery_handler import celery_app

@celery_app.task(bind=True)
def analyze_image(self, image_url: str):
    logging.info(f"Analyzing image: {image_url}")
    self.update_state(status="DOWNLOADING")

    logging.info(f"Downloaded image {image_url}")
    response = requests.get(image_url, timeout=10)
    response.raise_for_status()
    content_type = response.headers.get("Content-Type", "")
    if not content_type.startswith("image/"):
        raise ValueError("URL does not point to an image")

    self.update_state(status="ANALYZING")
    try:
        image_data = Image.open(BytesIO(response.content))
        image_data.verify()
    except UnidentifiedImageError:
        raise ValueError("Unable to identify image format")

    time.sleep(20)  # Simulate a long-running task
    return {
        "url": image_url,
        "format": image_data.format,
        "width": image_data.width,
        "height": image_data.height,
        "size": len(response.content),
    }

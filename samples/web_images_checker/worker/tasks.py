
import logging
import time

from .celery_handler import celery_app

@celery_app.task
def analyze_image(image_url: str):
    logging.info(f"Analyzing image: {image_url}")
    time.sleep(20)  # Simulate a long-running task
    return {
        "type": "image",
        "url": image_url
    }


import time
import logging
import requests
from io import BytesIO
from PIL import Image, UnidentifiedImageError

from worker.celery_handler import celery_app

MAX_IMAGE_SIZE = 1024 * 1024 * 5  # 5MB


@celery_app.task(bind=True)
def analyze_image(self, image_url: str):
    self.update_state(state="DOWNLOADING")
    logging.info(f"Downloading image {image_url}")

    with requests.get(image_url, stream=True, timeout=10) as response:
        response.raise_for_status()
        content_type = response.headers.get("Content-Type", "").lower()
        if content_type and not content_type.startswith("image/"):
            # If there is no Content-Type we try to read it and check the data later.
            raise ValueError("URL does not point to an image")

        data = BytesIO()
        total_size = 0
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                total_size += len(chunk)

                if total_size > MAX_IMAGE_SIZE:
                    raise ValueError(
                        "The image is too big. "
                        f"Maximum size is {MAX_IMAGE_SIZE / (1024 ** 2):.2f} MB."
                    )
                data.write(chunk)
        data.seek(0)  # Set the file pointer at the beginning of data

    self.update_state(state="ANALYZING")
    try:
        image_data = Image.open(data)
        image_data.verify()
    except (UnidentifiedImageError, OSError) as e:
        raise ValueError("Unable to identify image format") from e

    # Reopen is needed after image_data.verify()
    data.seek(0)
    image_data = Image.open(data)

    time.sleep(60)  # Simulate a long-running task
    return {
        "url": image_url,
        "format": image_data.format,
        "width": image_data.width,
        "height": image_data.height,
        "size": total_size,
    }

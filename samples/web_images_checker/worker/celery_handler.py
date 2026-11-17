from celery import Celery

celery_app = Celery(
    "web_image_checker_tasks",
    broker="redis://redis-web_images_checker:6379/0",
    backend="redis://redis-web_images_checker:6379/1",
    include=["worker.tasks"]
)

celery_app.conf.update(
    task_track_started=True,
    # result_expires=3600,
)

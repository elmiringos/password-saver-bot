# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=import-error
# pylint: disable=too-few-public-methods
import os
import time

from celery import Celery
from delete_msg import delete_msg

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")

@celery.task(name="create_task")
async def create_task(chat_id, msg_id, task_type):
    time.sleep(int(task_type) * 3)
    await delete_msg(chat_id, msg_id)
    return f"{msg_id} is deleted"

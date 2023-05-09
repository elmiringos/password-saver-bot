# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=import-error
# pylint: disable=too-few-public-methods
import celery

app = celery.Celery('tasks', broker='redis://127.0.0.1:6379')

@app.task
def delete_msg(arg):
    print(f"{arg} - deleted")

app.conf.beat_schedule = {
    'task-name': {
        'task': 'tasks.delete_msg',
        'schedule': 5.0,
        'args': (123),
    },
}

app.conf.timezone = 'UTC'

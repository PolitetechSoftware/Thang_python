from celery import Celery
from celery.schedules import crontab
from datetime import timedelta
import os 

# Create Celery instance
RABBITMQ_USER = os.getenv('RABBITMQ_USER') or "guest"
RABBITMQ_PORT = os.getenv('RABBITMQ_PORT') or 5672
SAVE_TASK_SCHEDULER = os.getenv('SAVE_DB_INTERVAL') or 5
SIMULATE_TASK_SCHEDULER = os.getenv('TASK_SIMULATE_INTERVAL') or 5


app = Celery('tasks', broker='amqp://{user}@rabbitmq:{port}/'.format(user=RABBITMQ_USER, port=RABBITMQ_PORT))

# Configure Celery Beat to schedule tasks
app.conf.beat_schedule = {
    'save-every-5-seconds': {
        'task': 'save_metrics_tasks.save_metrics_queue',  # save metrics 
        'schedule': timedelta(seconds=int(SAVE_TASK_SCHEDULER)),  # Run the task every SAVE_TASK_SCHEDULER seconds
    },
    'simulate-every-5-second': {
        'task': 'tasks.simulate_func_call',  # Call function
        'schedule': timedelta(seconds=int(SIMULATE_TASK_SCHEDULER)),  # Run the task every SIMULATE_TASK_SCHEDULER seconds
    },
}

# Optional: Celery configuration
app.conf.timezone = 'UTC'
from celery import Celery 
from time import sleep 

app = Celery("tasks", broker = "amqp://guest:guest@172.17.0.2:5672//")

@app.task
def reverse(text):
    sleep(5)
    return text[::-1]
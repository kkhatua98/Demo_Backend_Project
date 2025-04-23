>>> from celery import Celery
>>> app = Celery("tasks", broker = "amqp://guest:guest@localhost:5672//")
>>> from tasks import reverse
>>> app.send_task("tasks.reverse", args = ["ABCD"])
<AsyncResult: 8fe337c2-f55b-4e45-b8db-4c01b8161244>

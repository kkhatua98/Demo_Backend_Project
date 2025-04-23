FROM python:3
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY tasks.py tasks.py

CMD ["celery", "-A", "tasks", "worker", "--loglevel=info"]

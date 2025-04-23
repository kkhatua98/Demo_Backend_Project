FROM python:3.10-slim

# Install Tesseract and dependencies
RUN apt-get update && apt-get install -y tesseract-ocr 

# Copy files
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

# Default command
CMD ["celery", "-A", "ocr.app", "worker", "--loglevel=info"]

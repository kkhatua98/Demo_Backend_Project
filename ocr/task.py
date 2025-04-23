from celery import Celery
import os 
import ocr

BROKER_URL = os.environ.get("BROKER_URL", "amqp://")

app = Celery("tasks", broker = BROKER_URL)

@app.task(name="task")
def task(s3_image_path):
    # local_path = ocr.download_image(s3_image_path)
    # extracted_file_path = ocr.extract_text(local_path)
    # ocr.upload_text(extracted_file_path)
    # ocr.delete_files([local_path, extracted_file_path])

    local_image_path = ocr.download_image(s3_image_path)
    text = ocr.extract_text(local_image_path)
    doc_id = ocr.push_to_db(text)
    ocr.upload_text(text)
    ocr.delete_files([local_image_path])

    return {"id":doc_id, "status":"success"}

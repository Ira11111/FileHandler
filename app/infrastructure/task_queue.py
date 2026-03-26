import os

from celery import Celery

from ..infrastructure.nlp import generate_word_statistics
from app.config.config import REPORTS_DIR, load_config

config = load_config()
print("CONFIG", config.broker.broker_url, config.broker.backend_url)
celery_app = Celery(
    "celery_app", broker=config.broker.broker_url, backend=config.broker.backend_url
)

celery_app.conf.broker_transport_options = {'visibility_timeout': config.broker.visibility_timeout}


@celery_app.task(name="process_text_task", bind=True)
def process_text_task(self, input_filepath: str, task_id: str):
    """
    Фоновая задача Celery. Читает файл, собирает статистику, генерирует Excel.
    """

    original_name, _ = os.path.splitext(input_filepath)
    output_filepath = os.path.join(REPORTS_DIR, f"{task_id}_{original_name}_report.xlsx")

    try:
        generate_word_statistics(input_filepath, output_filepath)
        # Возвращаем путь для скачивания
        return {"download_url": f"/public/report/download/{task_id}"}
    except Exception as exc:
        raise self.retry(exc=exc, max_retries=config.broker.max_retries)
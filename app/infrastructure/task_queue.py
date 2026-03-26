import os
from ..infrastructure.nlp import generate_word_statistics
from app.main import REPORTS_DIR, celery_app, config

os.makedirs(REPORTS_DIR, exist_ok=True)


@celery_app.task(name="process_text_task", bind=True)
def process_text_task(self, input_filepath: str, task_id: str):
    """
    Фоновая задача Celery. Читает файл, собирает статистику, генерирует Excel.
    """
    output_filepath = os.path.join(REPORTS_DIR, f"{task_id}_report.xlsx")

    try:
        generate_word_statistics(input_filepath, output_filepath)
        # Возвращаем путь для скачивания
        return {"download_url": f"/public/report/download/{task_id}"}
    except Exception as exc:
        raise self.retry(exc=exc, max_retries=config.broker.max_retries)

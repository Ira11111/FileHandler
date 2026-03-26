import os
import shutil
import uuid
from fastapi import UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from celery.result import AsyncResult

from ..domain.entities import TaskResponse, TaskStatusEnum
from app.main import UPLOAD_DIR, REPORTS_DIR, app
from ..infrastructure.task_queue import process_text_task, celery_app

# Инициализируем приложение


# Папка для сохранения загруженных файлов
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/public/report/export", summary="Загрузить файл для анализа")
async def export_report(file: UploadFile = File(...)):
    """
    Принимает файл, сохраняет его на диск потоково и ставит задачу в очередь.
    """
    if not file.filename.endswith('.txt'):
        raise HTTPException(status_code=400, detail="Разрешены только файлы формата .txt")

    # Генерируем уникальный ID для задачи
    task_id = uuid.uuid4()

    # Формируем безопасное имя файла
    safe_filename = f"{task_id}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, safe_filename)

    try:
        # Сохраняем файл потоково (чанками).
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при сохранении файла: {str(e)}")
    finally:
        file.file.close()

    process_text_task.apply_async(args=[file_path, str(task_id)], task_id=str(task_id))

    return TaskResponse(
        task_id=str(task_id),
        status=TaskStatusEnum.PENDING,
        download_url=None
    )


@app.get("/public/report/status/{task_id}", summary="Проверить статус задачи")
async def get_status(task_id: str):
    result = AsyncResult(task_id, app=celery_app)

    # Маппинг стандартных статусов Celery в наши доменные статусы
    if result.state == 'PENDING':
        status = TaskStatusEnum.PENDING
    elif result.state in ('STARTED', 'PROGRESS'):
        status = TaskStatusEnum.PROCESSING
    elif result.state == 'SUCCESS':
        status = TaskStatusEnum.COMPLETED
    elif result.state == 'FAILURE':
        status = TaskStatusEnum.FAILED
    else:
        status = TaskStatusEnum.PROCESSING

    download_url = None
    # Если задача завершена успешно, отдаем ссылку на скачивание
    if status == TaskStatusEnum.COMPLETED:
        download_url = f"/public/report/download/{task_id}"

    return TaskResponse(
        task_id=task_id,
        status=status,
        download_url=download_url
    )


@app.get("/public/report/download/{task_id}", summary="Скачать готовый отчет")
async def download_report(task_id: str):
    """
    Отдает пользователю готовый Excel файл по ID задачи.
    """
    # Формируем путь к файлу, который должен был создать Celery
    file_path = os.path.join(REPORTS_DIR, f"{task_id}_report.xlsx")

    # Проверяем, существует ли физически этот файл
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail="Файл не найден. Возможно, задача еще выполняется или произошла ошибка."
        )

    return FileResponse(
        path=file_path,
        filename=f"report_{task_id}.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

import os
import time
import requests

from app.domain.entities import TaskStatusEnum
from utils.gen_file import gen_file

BASE_URL = "http://localhost:8000/public/report"


def test_e2e_upload_and_process_file():
    """
    1. Берем небольшой тестовый файл.
    2. Отправляем его в API.
    3. Получаем task_id.
    4. Опрашиваем статус, пока он не станет SUCCESS.
    5. Проверяем, что вернулась ссылка на скачивание.
    """


    # Отправляем файл на сервер
    upload_url = f"{BASE_URL}/export"
    file_path = gen_file(20000)
    with open(file_path, "rb") as f:
        response = requests.post(upload_url, files={"file": f})

    os.remove(file_path) # удаляем сгенерированный файл

    assert response.status_code ==201, f"Ошибка загрузки: {response.text}"

    data = response.json()
    assert "task_id" in data, "В ответе нет task_id!"
    task_id = data["task_id"]
    task_status = data["status"]
    assert task_status == TaskStatusEnum.PENDING, "Неверный статус при создании задачи"
    print(f"\nФайл загружен. Task ID: {task_id}")

    # Начинаем опрос статуса
    status_url = f"{BASE_URL}/status/{task_id}"

    max_retries = 30
    delay = 2

    result_data = {}

    for i in range(max_retries):
        status_response = requests.get(status_url)
        assert status_response.status_code == 200

        result_data = status_response.json()
        task_status = result_data.get("status")

        print(f"[{i + 1}/{max_retries}] Статус: {task_status}...")

        if task_status in [TaskStatusEnum.COMPLETED, TaskStatusEnum.FAILED]:
            break

        time.sleep(delay)

    # Проверяем финальный результат
    assert task_status == TaskStatusEnum.COMPLETED, f"Задача завершилась с ошибкой: {result_data}"

    # Проверяем, что воркер вернул то, что мы писали в task_queue.py
    assert "download_url" in result_data.get("result", result_data), "Нет ссылки на скачивание!"
    print(f"Тест успешно пройден! Ссылка: {result_data.get('download_url', result_data.get('result'))}")
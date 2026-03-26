import os

import uvicorn
from celery import Celery
from fastapi import FastAPI

from app.config.config import load_config

REPORTS_DIR = os.path.join(os.getcwd(), "data", "reports")
UPLOAD_DIR = os.path.join(os.getcwd(), "data", "uploads")

config = load_config()
app = FastAPI(
    title="Word Frequency Analyzer API",
    description="API для асинхронного анализа частотности слов в текстах"
)

celery_app = Celery(
    "celery_app", broker=config.broker.broker_url, backend=config.broker.backend_url
)
celery_app.conf.broker_transport_options = {'visibility_timeout': config.broker.visibility_timeout}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=config.http.host,
        port=8000,
        reload=True
    )

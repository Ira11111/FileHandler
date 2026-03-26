import uvicorn
from fastapi import FastAPI

from app.config.config import load_config
from app.api.report_api import router

config = load_config()
app = FastAPI(
    title="Word Frequency Analyzer API",
    description="API для асинхронного анализа частотности слов в текстах"
)
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=config.http.host,
        port=8000,
        reload=True
    )

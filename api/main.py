# api/main.py

from fastapi import FastAPI
import uvicorn

from api.routers import notion_router
from api.utils.helpers import logger

app = FastAPI(
    title="AI Life Coach API",
    version="1.0",
    description="An API server for AI life coach interactions"
)

app.include_router(notion_router)

if __name__ == "__main__":
    logger.info("Starting AI Life Coach API server...")
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)

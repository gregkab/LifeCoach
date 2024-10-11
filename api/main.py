# api/main.py

from fastapi import FastAPI
import uvicorn
from api.notion_logic import router as notion_router

app = FastAPI(
    title="AI Life Coach API",
    version="1.0",
    description="An API server for AI life coach interactions"
)

app.include_router(notion_router)

if __name__ == "__main__":
    uvicorn.run("api.main:app", host="localhost", port=8000, reload=True)

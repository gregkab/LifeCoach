# api/routers/notion_logic.py

import datetime
from fastapi import APIRouter, Depends, HTTPException

from api.models.log_models import LogEntry, FeedbackRequest
from api.services.notion_service import NotionService
from api.services.feedback_service import FeedbackService

router = APIRouter()

@router.get("/daily_logs")
async def get_daily_logs(service: NotionService = Depends()):
    today = datetime.date.today().isoformat()
    logs = await service.fetch_logs_for_date_range(today, today)
    return {"logs": logs}

@router.get("/weekly_logs")
async def get_weekly_logs(service: NotionService = Depends()):
    today = datetime.date.today()
    one_week_ago = (today - datetime.timedelta(days=6)).isoformat()
    today_str = today.isoformat()
    logs = await service.fetch_logs_for_date_range(one_week_ago, today_str)
    return {"logs": logs}

@router.get("/logs")
async def fetch_logs(goal_status: str = None, service: NotionService = Depends()):
    return await service.get_logs(goal_status)

@router.post("/logs")
async def add_log(entry: LogEntry, service: NotionService = Depends()):
    return await service.create_log(entry)

@router.post("/feedback")
async def generate_feedback(request: FeedbackRequest, feedback_service: FeedbackService = Depends()):
    return await feedback_service.generate_feedback(request)

@router.post("/daily_feedback")
async def generate_daily_feedback(service: NotionService = Depends(), feedback_service: FeedbackService = Depends()):
    today_str = datetime.date.today().isoformat()
    logs = await service.fetch_logs_for_date_range(today_str, today_str)
    return await feedback_service.generate_daily_feedback(logs)

@router.post("/weekly_feedback")
async def generate_weekly_feedback(service: NotionService = Depends(), feedback_service: FeedbackService = Depends()):
    today = datetime.date.today()
    one_week_ago_str = (today - datetime.timedelta(days=6)).isoformat()
    today_str = today.isoformat()
    logs = await service.fetch_logs_for_date_range(one_week_ago_str, today_str)
    return await feedback_service.generate_weekly_feedback(logs)

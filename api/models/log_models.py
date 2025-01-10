# api/models/log_models.py

from pydantic import BaseModel

class LogEntry(BaseModel):
    date: str
    thoughts: str
    goals: str
    reflections: str
    goal_status: str

class FeedbackRequest(BaseModel):
    thoughts: str
    goals: str
    reflections: str

import datetime
from fastapi import APIRouter, HTTPException
from notion_client import Client
from pydantic import BaseModel
from dotenv import load_dotenv
import os

from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

# Load environment variables
load_dotenv()
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.environ["LANGCHAIN_API_KEY"]
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

# Initialize Notion client
notion = Client(auth=NOTION_TOKEN)

# Initialize API Router
router = APIRouter()

# Data Models
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

# Helper function to fetch logs within a date range
async def fetch_logs_for_date_range(start_date: str, end_date: str):
    try:
        response = notion.databases.query(
            database_id=DATABASE_ID,
            filter={
                "property": "Date",
                "date": {
                    "on_or_after": start_date,
                    "on_or_before": end_date
                }
            }
        )
        logs = []
        for page in response['results']:
            date_property = page['properties'].get('Date')
            date = 'No Date'
            if date_property and 'date' in date_property and date_property['date']:
                date = date_property['date'].get('start', 'No Date')

            thoughts_property = page['properties'].get('Thoughts', {}).get('rich_text', [])
            thoughts = 'No Thoughts'
            if thoughts_property and len(thoughts_property) > 0:
                thoughts = thoughts_property[0].get('plain_text', 'No Thoughts')

            goals_property = page['properties'].get('Goals', {}).get('rich_text', [])
            goals = 'No Goals'
            if goals_property and len(goals_property) > 0:
                goals = goals_property[0].get('plain_text', 'No Goals')

            reflections_property = page['properties'].get('Reflections', {}).get('rich_text', [])
            reflections = 'No Reflections'
            if reflections_property and len(reflections_property) > 0:
                reflections = reflections_property[0].get('plain_text', 'No Reflections')

            # New goal_status extraction
            goal_status_property = page['properties'].get('Goal Status', {}).get('select', {}).get('name', 'Not Specified')

            logs.append({
                "date": date,
                "thoughts": thoughts,
                "goals": goals,
                "reflections": reflections,
                "goal_status": goal_status_property  # Add goal_status to logs
            })
        return logs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to fetch daily logs
@router.get("/daily_logs")
async def get_daily_logs():
    today = datetime.date.today().isoformat()
    return await fetch_logs_for_date_range(today, today)

# Endpoint to fetch weekly logs
@router.get("/weekly_logs")
async def get_weekly_logs():
    today = datetime.date.today()
    one_week_ago = (today - datetime.timedelta(days=6)).isoformat()
    today_str = today.isoformat()
    return await fetch_logs_for_date_range(one_week_ago, today_str)

# Endpoint to fetch all logs with goal status filtering
@router.get("/logs")
async def fetch_logs(goal_status: str = None):
    try:
        response = notion.databases.query(
            database_id=DATABASE_ID,
            filter={
                "property": "Goal Status",
                "select": {
                    "equals": goal_status
                }
            } if goal_status else None  # Apply filter only if goal_status is provided
        )
        logs = []
        for page in response['results']:
            date_property = page['properties'].get('Date')
            date = 'No Date'
            if date_property and 'date' in date_property and date_property['date']:
                date = date_property['date'].get('start', 'No Date')

            thoughts_property = page['properties'].get('Thoughts', {}).get('rich_text', [])
            thoughts = 'No Thoughts'
            if thoughts_property and len(thoughts_property) > 0:
                thoughts = thoughts_property[0].get('plain_text', 'No Thoughts')

            goals_property = page['properties'].get('Goals', {}).get('rich_text', [])
            goals = 'No Goals'
            if goals_property and len(goals_property) > 0:
                goals = goals_property[0].get('plain_text', 'No Goals')

            reflections_property = page['properties'].get('Reflections', {}).get('rich_text', [])
            reflections = 'No Reflections'
            if reflections_property and len(reflections_property) > 0:
                reflections = reflections_property[0].get('plain_text', 'No Reflections')

            goal_status_property = page['properties'].get('Goal Status', {}).get('select', {}).get('name', 'Not Specified')

            logs.append({
                "date": date,
                "thoughts": thoughts,
                "goals": goals,
                "reflections": reflections,
                "goal_status": goal_status_property
            })
        return {"logs": logs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to add a log with goal status
@router.post("/logs")
async def add_log(entry: LogEntry):
    try:
        notion.pages.create(
            parent={"database_id": DATABASE_ID},
            properties={
                "Date": {"date": {"start": entry.date}},
                "Thoughts": {"rich_text": [{"text": {"content": entry.thoughts}}]},
                "Goals": {"rich_text": [{"text": {"content": entry.goals}}]},
                "Reflections": {"rich_text": [{"text": {"content": entry.reflections}}]},
                "Goal Status": {"select": {"name": entry.goal_status}}  # New goal status property
            }
        )
        return {"message": "Log entry added successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/feedback")
async def generate_feedback(request: FeedbackRequest):
    try:
        # Initialize the ChatOpenAI model
        llm = ChatOpenAI(model="gpt-4", temperature=0, openai_api_key=OPENAI_API_KEY)

        # Create the prompt template
        prompt = ChatPromptTemplate.from_template(
            "Here are my thoughts: {thoughts}. My goals: {goals}. My reflections: {reflections}. "
            "Please provide feedback and suggestions to improve my productivity and help me achieve my goals."
        )
        chain = prompt | llm | StrOutputParser()
        feedback = chain.invoke({"thoughts": request.thoughts, "goals": request.goals, "reflections": request.reflections})

        return {"feedback": feedback}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@router.post("/daily_feedback")
async def generate_daily_feedback(request: FeedbackRequest):
    try:
        llm = ChatOpenAI(model="gpt-4", temperature=0, openai_api_key=OPENAI_API_KEY)

        # Create a prompt specifically for daily feedback
        prompt = ChatPromptTemplate.from_template(
            "Today, I had the following thoughts: {thoughts}. My goals were: {goals}. "
            "My reflections include: {reflections}. Based on these, provide immediate feedback and suggestions "
            "to help me make progress on my goals and improve my productivity tomorrow."
        )
        chain = prompt | llm | StrOutputParser()
        feedback = chain.invoke({
            "thoughts": request.thoughts,
            "goals": request.goals,
            "reflections": request.reflections
        })

        return {"feedback": feedback}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Weekly Feedback Endpoint
@router.post("/weekly_feedback")
async def generate_weekly_feedback(request: WeeklyFeedbackRequest):
    try:
        llm = ChatOpenAI(model="gpt-4", temperature=0, openai_api_key=OPENAI_API_KEY)

        # Aggregated prompt for weekly insights
        prompt = ChatPromptTemplate.from_template(
            "This past week, my daily thoughts were: {thoughts}. My goals over the week included: {goals}. "
            "Across these days, I reflected on the following: {reflections}. "
            "Based on this weekly review, provide a summary of my top achievements, recurring challenges, "
            "and actionable strategies to help me stay on track and improve my productivity in the upcoming week."
        )

        # Combine thoughts, goals, and reflections for the week
        combined_thoughts = "; ".join(request.thoughts)
        combined_goals = "; ".join(request.goals)
        combined_reflections = "; ".join(request.reflections)

        chain = prompt | llm | StrOutputParser()
        feedback = chain.invoke({
            "thoughts": combined_thoughts,
            "goals": combined_goals,
            "reflections": combined_reflections
        })

        return {"feedback": feedback}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
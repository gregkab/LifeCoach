#api/notion_logic.py
import os
import datetime
from fastapi import APIRouter, HTTPException
from notion_client import Client
from pydantic import BaseModel
from dotenv import load_dotenv

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
    date: str
    thoughts: str
    goals: str
    reflections: str
    goal_status: str

llm = ChatOpenAI(model="gpt-4o", temperature=0, openai_api_key=OPENAI_API_KEY)

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
            goal_status_property = page['properties'].get('Goal Status', {}).get('select', {})
            goal_status = 'Not Specified'
            if goal_status_property and 'name' in goal_status_property:
                goal_status = goal_status_property.get('name', 'Not Specified')

            logs.append({
                "date": date,
                "thoughts": thoughts,
                "goals": goals,
                "reflections": reflections,
                "goal_status": goal_status  # Add goal_status to logs
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
    
# Function to format logs for the prompt
def format_logs_for_prompt(logs):
    formatted_logs = ""
    for log in logs:
        formatted_logs += (
            f"Date: {log['date']}, "
            f"Thoughts: {log['thoughts']}, "
            f"Goals: {log['goals']} (Status: {log['goal_status']}), "
            f"Reflections: {log['reflections']}\n"
        )
    return formatted_logs

# Daily Feedback Endpoint
@router.post("/daily_feedback")
async def generate_daily_feedback():
    try:
        # Fetch today's logs
        today_str = datetime.date.today().isoformat()
        logs = await fetch_logs_for_date_range(today_str, today_str)

        if not logs:
            return {"feedback": "No logs found for today."}

        # Format logs for prompt
        formatted_logs = format_logs_for_prompt(logs)

        # Enhanced daily feedback prompt
        prompt = ChatPromptTemplate.from_template(
            "Here are my logs for today:\n{logs}\n"
            "Based on these entries, provide clear, direct steps I should take right now to improve my day and reach my goals. "
            "Be specific: tell me exactly what actions to take, even if they're small or involve mindset changes. "
            "Make it clear, like you’re walking me through every step of what a successful day would look like. "
            "Include motivation that reminds me why these steps will help me achieve my best self."
        )

        # Generate feedback
        chain = prompt | llm | StrOutputParser()
        feedback = chain.invoke({"logs": formatted_logs})
        return {"feedback": feedback}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Weekly Feedback Endpoint
@router.post("/weekly_feedback")
async def generate_weekly_feedback():
    try:
        # Fetch logs for the past week
        today = datetime.date.today()
        one_week_ago_str = (today - datetime.timedelta(days=6)).isoformat()
        logs = await fetch_logs_for_date_range(one_week_ago_str, today.isoformat())

        if not logs:
            return {"feedback": "No logs found for the past week."}

        # Format logs for prompt
        formatted_logs = format_logs_for_prompt(logs)

        # Enhanced weekly feedback prompt
        prompt = ChatPromptTemplate.from_template(
            "Here are my logs for the past week:\n{logs}\n"
            "Based on these entries, provide a detailed plan for me to follow next week. "
            "Identify any recurring patterns, highlight what worked well, and point out areas where I struggled. "
            "Give me a step-by-step roadmap with specific actions to take each day or across the week. "
            "Make each action concrete, and explain why these steps will maximize my progress. "
            "Think like a life coach focused on ensuring my success, guiding me toward a powerful, fulfilling week."
        )

        # Generate feedback
        chain = prompt | llm | StrOutputParser()
        feedback = chain.invoke({"logs": formatted_logs})
        return {"feedback": feedback}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
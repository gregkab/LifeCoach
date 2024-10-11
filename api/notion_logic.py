# api/notion_logic.py

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

class FeedbackRequest(BaseModel):
    thoughts: str
    goals: str
    reflections: str

# API Endpoints

@router.get("/logs")
async def fetch_logs():
    try:
        response = notion.databases.query(database_id=DATABASE_ID)
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

            logs.append({
                "date": date,
                "thoughts": thoughts,
                "goals": goals,
                "reflections": reflections
            })
        return {"logs": logs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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

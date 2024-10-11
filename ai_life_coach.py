from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from notion_client import Client
from dotenv import load_dotenv
import os
import datetime

# Load environment variables from .env file
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
notion_token = os.getenv("NOTION_TOKEN")

# Initialize the Notion client
notion = Client(auth=notion_token)

# Replace with your Notion database ID
database_id = "102f2c4892e980dd9005cc5c9489ba82"

# Function to fetch daily logs from Notion using LangChain
def fetch_daily_logs():
    response = notion.databases.query(database_id=database_id)
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

        logs.append(f"Date: {date}, Thoughts: {thoughts}")
    return logs

# Function to add a new daily log to Notion using LangChain
def add_daily_log(date, thoughts, goals, reflections):
    notion.pages.create(
        parent={"database_id": database_id},
        properties={
            "Date": {"date": {"start": date}},
            "Thoughts": {"rich_text": [{"text": {"content": thoughts}}]},
            "Goals": {"rich_text": [{"text": {"content": goals}}]},
            "Reflections": {"rich_text": [{"text": {"content": reflections}}]},
        }
    )

# Function to generate AI-based feedback using GPT-4 via LangChain
def generate_feedback(thoughts, goals, reflections):
    model = ChatOpenAI(model="gpt-4", temperature=0)
    prompt = ChatPromptTemplate.from_template(
        "Here are my thoughts: {thoughts}. My goals: {goals}. My reflections: {reflections}. "
        "Please provide feedback and suggestions to improve my productivity and help me achieve my goals."
    )
    chain = prompt | model | StrOutputParser()
    
    feedback = chain.invoke({"thoughts": thoughts, "goals": goals, "reflections": reflections})
    return feedback

# Example usage
if __name__ == "__main__":
    # Fetch existing logs
    logs = fetch_daily_logs()
    for log in logs:
        print(log)

    # Add a new log and generate feedback from GPT-4
    date = str(datetime.date.today())
    thoughts = "I worked on my AI Life Coach project today."
    goals = "Finish the Notion integration."
    reflections = "Made good progress but need to work on better time management."

    add_daily_log(date, thoughts, goals, reflections)

    # Generate and print AI feedback
    feedback = generate_feedback(thoughts, goals, reflections)
    print(f"\nAI Feedback: {feedback}")

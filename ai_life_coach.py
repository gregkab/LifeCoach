from notion_client import Client
from dotenv import load_dotenv
import os
import datetime

# Load environment variables from .env file
load_dotenv()

# Get the Notion token from environment variables
notion_token = os.getenv("NOTION_TOKEN")

# Initialize the Notion client with the token
notion = Client(auth=notion_token)

# Replace with your Notion database ID
database_id = "102f2c4892e980dd9005cc5c9489ba82"

# Function to fetch daily logs from Notion
def fetch_daily_logs():
    response = notion.databases.query(database_id=database_id)
    for page in response['results']:
        # Check if 'Date' property exists and has a 'date' value
        date_property = page['properties'].get('Date')
        date = 'No Date'  # Default value
        if date_property and 'date' in date_property and date_property['date']:
            date = date_property['date'].get('start', 'No Date')

        # Check if 'Thoughts' property exists and has 'rich_text'
        thoughts_property = page['properties'].get('Thoughts', {}).get('rich_text', [])
        thoughts = 'No Thoughts'  # Default value
        if thoughts_property and len(thoughts_property) > 0:
            thoughts = thoughts_property[0].get('plain_text', 'No Thoughts')

        print(f"Date: {date}, Thoughts: {thoughts}")


# Function to add a new daily log to Notion
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

# Example usage
if __name__ == "__main__":
    # Fetch existing logs
    fetch_daily_logs()
    
    # Add a new log (you can modify the date and content)
    add_daily_log(str(datetime.date.today()), "Worked on AI Life Coach project.", "Understand Notion API", "Good progress.")

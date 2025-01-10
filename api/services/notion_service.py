# api/services/notion_service.py

import os
import datetime
from typing import List, Optional

from fastapi import HTTPException
from notion_client import Client

from api.models.log_models import LogEntry
from api.utils.helpers import logger

class NotionService:
    def __init__(self):
        self.notion = Client(auth=os.getenv("NOTION_TOKEN"))
        self.database_id = os.getenv("NOTION_DATABASE_ID")
        if not self.database_id:
            logger.error("NOTION_DATABASE_ID is not set in environment variables.")
            raise ValueError("NOTION_DATABASE_ID is not configured.")
    
    async def fetch_logs_for_date_range(self, start_date: str, end_date: str) -> List[dict]:
        try:
            logger.info(f"Fetching logs from {start_date} to {end_date}")
            response = self.notion.databases.query(
                database_id=self.database_id,
                filter={
                    "and": [
                        {
                            "property": "Date",
                            "date": {
                                "on_or_after": start_date
                            }
                        },
                        {
                            "property": "Date",
                            "date": {
                                "on_or_before": end_date
                            }
                        }
                    ]
                }
            )
            logs = self._process_logs(response['results'])
            return logs
        except Exception as e:
            logger.error(f"Error fetching logs: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def get_logs(self, goal_status: Optional[str] = None) -> dict:
        try:
            logger.info(f"Fetching logs with goal_status: {goal_status}")
            filter_clause = (
                {
                    "property": "Goal Status",
                    "select": {
                        "equals": goal_status
                    }
                } if goal_status else None
            )
    
            query_params = {"database_id": self.database_id}
            if filter_clause:
                query_params["filter"] = filter_clause
    
            response = self.notion.databases.query(**query_params)
            logs = self._process_logs(response['results'])
            return {"logs": logs}
        except Exception as e:
            logger.error(f"Error fetching logs: {e}")
            raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    
    def _process_logs(self, pages) -> List[dict]:
        logs = []
        for page in pages:
            log = {
                "date": self._extract_date(page),
                "thoughts": self._extract_text(page, 'Thoughts'),
                "goals": self._extract_text(page, 'Goals'),
                "reflections": self._extract_text(page, 'Reflections'),
                "goal_status": self._extract_goal_status(page)
            }
            logs.append(log)
        logger.debug(f"Processed {len(logs)} logs")
        return logs
    
    def _extract_date(self, page) -> str:
        date_property = page['properties'].get('Date', {}).get('date', {})
        return date_property.get('start', 'No Date') if date_property else 'No Date'
    
    def _extract_text(self, page, property_name: str) -> str:
        property_value = page['properties'].get(property_name, {}).get('rich_text', [])
        if property_value and len(property_value) > 0:
            return property_value[0].get('plain_text', f'No {property_name}')
        return f'No {property_name}'
    
    def _extract_goal_status(self, page) -> str:
        goal_status_property = page['properties'].get('Goal Status', {}).get('select', {})
        return goal_status_property.get('name', 'Not Specified') if goal_status_property else 'Not Specified'
    
    async def create_log(self, entry: LogEntry) -> dict:
        try:
            logger.info(f"Adding new log entry: {entry}")
            self.notion.pages.create(
                parent={"database_id": self.database_id},
                properties={
                    "Date": {"date": {"start": entry.date}},
                    "Thoughts": {"rich_text": [{"text": {"content": entry.thoughts}}]},
                    "Goals": {"rich_text": [{"text": {"content": entry.goals}}]},
                    "Reflections": {"rich_text": [{"text": {"content": entry.reflections}}]},
                    "Goal Status": {"select": {"name": entry.goal_status}}
                }
            )
            logger.info("Log entry added successfully.")
            return {"message": "Log entry added successfully."}
        except Exception as e:
            logger.error(f"Error adding log entry: {e}")
            raise HTTPException(status_code=500, detail=str(e))

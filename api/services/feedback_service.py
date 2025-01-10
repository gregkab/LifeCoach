# api/services/feedback_service.py

import os
from typing import List

from fastapi import HTTPException

from api.models.log_models import FeedbackRequest
from api.utils.helpers import logger

from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

class FeedbackService:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key:
            logger.error("OPENAI_API_KEY is not set in environment variables.")
            raise ValueError("OPENAI_API_KEY is not configured.")
        
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0, openai_api_key=self.openai_api_key)
        logger.info("FeedbackService initialized with GPT-4 model.")
    
    async def generate_feedback(self, request: FeedbackRequest) -> dict:
        try:
            logger.info("Generating feedback based on user request.")
            prompt = ChatPromptTemplate.from_template(
                "Here are my thoughts: {thoughts}. My goals: {goals}. My reflections: {reflections}. "
                "Please provide feedback and suggestions to improve my productivity and help me achieve my goals."
            )
            chain = prompt | self.llm | StrOutputParser()
            feedback = chain.invoke({
                "thoughts": request.thoughts,
                "goals": request.goals,
                "reflections": request.reflections
            })
            logger.debug(f"Generated feedback: {feedback}")
            return {"feedback": feedback}
        except Exception as e:
            logger.error(f"Error generating feedback: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    def format_logs_for_prompt(self, logs: List[dict]) -> str:
        formatted_logs = ""
        for log in logs:
            formatted_logs += (
                f"Date: {log['date']}, "
                f"Thoughts: {log['thoughts']}, "
                f"Goals: {log['goals']} (Status: {log['goal_status']}), "
                f"Reflections: {log['reflections']}\n"
            )
        logger.debug("Formatted logs for prompt.")
        return formatted_logs
    
    async def generate_daily_feedback(self, logs: List[dict]) -> dict:
        try:
            logger.info("Generating daily feedback.")
            if not logs:
                return {"feedback": "No logs found for today."}
    
            formatted_logs = self.format_logs_for_prompt(logs)
    
            prompt = ChatPromptTemplate.from_template(
                "Here are my logs for today:\n{logs}\n"
                "Based on these entries, provide clear, direct steps I should take right now to improve my day and reach my goals. "
                "Be specific: tell me exactly what actions to take, even if they're small or involve mindset changes. "
                "Make it clear, like you’re walking me through every step of what a successful day would look like. "
                "Include motivation that reminds me why these steps will help me achieve my best self."
            )
    
            chain = prompt | self.llm | StrOutputParser()
            feedback = chain.invoke({"logs": formatted_logs})
            logger.debug(f"Generated daily feedback: {feedback}")
            return {"feedback": feedback}
        except Exception as e:
            logger.error(f"Error generating daily feedback: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def generate_weekly_feedback(self, logs: List[dict]) -> dict:
        try:
            logger.info("Generating weekly feedback.")
            if not logs:
                return {"feedback": "No logs found for the past week."}
    
            formatted_logs = self.format_logs_for_prompt(logs)
    
            prompt = ChatPromptTemplate.from_template(
                "Here are my logs for the past week:\n{logs}\n"
                "Based on these entries, provide a detailed plan for me to follow next week. "
                "Identify any recurring patterns, highlight what worked well, and point out areas where I struggled. "
                "Give me a step-by-step roadmap with specific actions to take each day or across the week. "
                "Make each action concrete, and explain why these steps will maximize my progress. "
                "Think like a life coach focused on ensuring my success, guiding me toward a powerful, fulfilling week."
            )
    
            chain = prompt | self.llm | StrOutputParser()
            feedback = chain.invoke({"logs": formatted_logs})
            logger.debug(f"Generated weekly feedback: {feedback}")
            return {"feedback": feedback}
        except Exception as e:
            logger.error(f"Error generating weekly feedback: {e}")
            raise HTTPException(status_code=500, detail=str(e))

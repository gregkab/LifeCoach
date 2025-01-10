# client/cli/commands.py

import requests
import datetime

API_URL = "http://localhost:8000"

def fetch_logs(goal_status=None):
    params = {"goal_status": goal_status} if goal_status else {}
    try:
        response = requests.get(f"{API_URL}/logs", params=params)
        response.raise_for_status()
        logs = response.json().get('logs', [])
        if not logs:
            print("No logs found.")
            return
        for log in logs:
            print(f"Date: {log['date']}, Thoughts: {log['thoughts']}, "
                  f"Goals: {log['goals']} (Status: {log['goal_status']}), "
                  f"Reflections: {log['reflections']}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch logs: {e}")

def fetch_daily_logs():
    try:
        response = requests.get(f"{API_URL}/daily_logs")
        response.raise_for_status()
        logs = response.json().get('logs', [])
        if not logs:
            print("No daily logs found.")
            return
        for log in logs:
            print(f"Date: {log['date']}, Thoughts: {log['thoughts']}, "
                  f"Goals: {log['goals']} (Status: {log.get('goal_status', 'Not Specified')}), "
                  f"Reflections: {log['reflections']}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch daily logs: {e}")

def fetch_weekly_logs():
    try:
        response = requests.get(f"{API_URL}/weekly_logs")
        response.raise_for_status()
        logs = response.json().get('logs', [])
        if not logs:
            print("No weekly logs found.")
            return
        for log in logs:
            print(f"Date: {log['date']}, Thoughts: {log['thoughts']}, "
                  f"Goals: {log['goals']} (Status: {log.get('goal_status', 'Not Specified')}), "
                  f"Reflections: {log['reflections']}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch weekly logs: {e}")

def add_log():
    date = str(datetime.date.today())
    thoughts = input("Enter your thoughts: ")
    goals = input("Enter your goals: ")
    reflections = input("Enter your reflections: ")
    goal_status = input("Enter the goal status (pending, in progress, completed): ")

    data = {
        "date": date,
        "thoughts": thoughts,
        "goals": goals,
        "reflections": reflections,
        "goal_status": goal_status
    }

    try:
        response = requests.post(f"{API_URL}/logs", json=data)
        response.raise_for_status()
        print("Log entry added successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to add log entry: {e}")

def get_daily_feedback():
    try:
        response = requests.post(f"{API_URL}/daily_feedback")
        response.raise_for_status()
        feedback = response.json().get('feedback', '')
        print(f"\nAI Daily Feedback: {feedback}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to get daily feedback: {e}")

def get_weekly_feedback():
    try:
        response = requests.post(f"{API_URL}/weekly_feedback")
        response.raise_for_status()
        feedback = response.json().get('feedback', '')
        print(f"\nAI Weekly Feedback: {feedback}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to get weekly feedback: {e}")

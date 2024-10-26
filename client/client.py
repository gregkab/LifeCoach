# client/client.py

import requests
import datetime

API_URL = "http://localhost:8000"

def fetch_logs(goal_status=None):
    params = {"goal_status": goal_status} if goal_status else {}
    response = requests.get(f"{API_URL}/logs", params=params)
    if response.status_code == 200:
        logs = response.json().get('logs', [])
        for log in logs:
            print(f"Date: {log['date']}, Thoughts: {log['thoughts']}, Goals: {log['goals']}, Reflections: {log['reflections']}, Goal Status: {log['goal_status']}")
    else:
        print("Failed to fetch logs.")

def fetch_daily_logs():
    response = requests.get(f"{API_URL}/daily_logs")
    if response.status_code == 200:
        logs = response.json()
        for log in logs:
            print(f"Date: {log['date']}, Thoughts: {log['thoughts']}, Goals: {log['goals']}, Reflections: {log['reflections']}, Goal Status: {log.get('goal_status', 'Not Specified')}")
    else:
        print("Failed to fetch daily logs.")

def fetch_weekly_logs():
    response = requests.get(f"{API_URL}/weekly_logs")
    if response.status_code == 200:
        logs = response.json()
        for log in logs:
            print(f"Date: {log['date']}, Thoughts: {log['thoughts']}, Goals: {log['goals']}, Reflections: {log['reflections']}, Goal Status: {log.get('goal_status', 'Not Specified')}")
    else:
        print("Failed to fetch weekly logs.")

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

    response = requests.post(f"{API_URL}/logs", json=data)
    if response.status_code == 200:
        print("Log entry added successfully.")
    else:
        print("Failed to add log entry.")

def get_feedback():
    thoughts = input("Enter your thoughts: ")
    goals = input("Enter your goals: ")
    reflections = input("Enter your reflections: ")

    data = {
        "thoughts": thoughts,
        "goals": goals,
        "reflections": reflections
    }

    response = requests.post(f"{API_URL}/feedback", json=data)
    if response.status_code == 200:
        feedback = response.json().get('feedback', '')
        print(f"\nAI Feedback: {feedback}")
    else:
        print("Failed to get feedback.")

if __name__ == "__main__":
    while True:
        print("\n1. Fetch All Logs")
        print("2. Fetch Daily Logs")
        print("3. Fetch Weekly Logs")
        print("4. Add Log")
        print("5. Get Feedback")
        print("6. Exit")
        choice = input("Select an option: ")
        
        if choice == '1':
            goal_status = input("Filter by goal status (pending, in progress, completed) or leave blank for all: ")
            fetch_logs(goal_status if goal_status else None)
        elif choice == '2':
            fetch_daily_logs()
        elif choice == '3':
            fetch_weekly_logs()
        elif choice == '4':
            add_log()
        elif choice == '5':
            get_feedback()
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")

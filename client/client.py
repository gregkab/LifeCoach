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
            print(f"Date: {log['date']}, Thoughts: {log['thoughts']}, "
                  f"Goals: {log['goals']} (Status: {log['goal_status']}), "
                  f"Reflections: {log['reflections']}")
    else:
        print("Failed to fetch logs.")

def fetch_daily_logs():
    response = requests.get(f"{API_URL}/daily_logs")
    if response.status_code == 200:
        logs = response.json()
        for log in logs:
            print(f"Date: {log['date']}, Thoughts: {log['thoughts']}, "
                  f"Goals: {log['goals']} (Status: {log.get('goal_status', 'Not Specified')}), "
                  f"Reflections: {log['reflections']}")
    else:
        print("Failed to fetch daily logs.")

def fetch_weekly_logs():
    response = requests.get(f"{API_URL}/weekly_logs")
    if response.status_code == 200:
        logs = response.json()
        for log in logs:
            print(f"Date: {log['date']}, Thoughts: {log['thoughts']}, "
                  f"Goals: {log['goals']} (Status: {log.get('goal_status', 'Not Specified')}), "
                  f"Reflections: {log['reflections']}")
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

def get_daily_feedback():
    response = requests.post(f"{API_URL}/daily_feedback")
    if response.status_code == 200:
        feedback = response.json().get('feedback', '')
        print(f"\nAI Daily Feedback: {feedback}")
    else:
        print("Failed to get daily feedback.")

def get_weekly_feedback():
    response = requests.post(f"{API_URL}/weekly_feedback")
    if response.status_code == 200:
        feedback = response.json().get('feedback', '')
        print(f"\nAI Weekly Feedback: {feedback}")
    else:
        print("Failed to get weekly feedback.")

if __name__ == "__main__":
    while True:
        print("\n1. Fetch All Logs")
        print("2. Fetch Daily Logs")
        print("3. Fetch Weekly Logs")
        print("4. Add Log")
        print("5. Get Daily Feedback")
        print("6. Get Weekly Feedback")
        print("7. Exit")
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
            get_daily_feedback()
        elif choice == '6':
            get_weekly_feedback()
        elif choice == '7':
            break
        else:
            print("Invalid choice. Please try again.")

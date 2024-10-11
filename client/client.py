# client/client.py

import requests
import datetime

API_URL = "http://localhost:8000"

def fetch_logs():
    response = requests.get(f"{API_URL}/logs")
    if response.status_code == 200:
        logs = response.json().get('logs', [])
        for log in logs:
            print(f"Date: {log['date']}, Thoughts: {log['thoughts']}, Goals: {log['goals']}, Reflections: {log['reflections']}")
    else:
        print("Failed to fetch logs.")

def add_log():
    date = str(datetime.date.today())
    thoughts = input("Enter your thoughts: ")
    goals = input("Enter your goals: ")
    reflections = input("Enter your reflections: ")

    data = {
        "date": date,
        "thoughts": thoughts,
        "goals": goals,
        "reflections": reflections
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
        print("\n1. Fetch Logs")
        print("2. Add Log")
        print("3. Get Feedback")
        print("4. Exit")
        choice = input("Select an option: ")
        if choice == '1':
            fetch_logs()
        elif choice == '2':
            add_log()
        elif choice == '3':
            get_feedback()
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

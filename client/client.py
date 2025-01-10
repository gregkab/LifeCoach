# client/client.py

from cli import (
    fetch_logs,
    fetch_daily_logs,
    fetch_weekly_logs,
    add_log,
    get_daily_feedback,
    get_weekly_feedback
)
from utils import clear_screen

def display_menu():
    print("\n===== AI Life Coach Client =====")
    print("1. Fetch All Logs")
    print("2. Fetch Daily Logs")
    print("3. Fetch Weekly Logs")
    print("4. Add Log")
    print("5. Get Daily Feedback")
    print("6. Get Weekly Feedback")
    print("7. Exit")

def main():
    while True:
        display_menu()
        choice = input("Select an option: ").strip()

        if choice == '1':
            goal_status = input("Filter by goal status (pending, in progress, completed) or leave blank for all: ").strip()
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
            print("Exiting the client. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

        input("\nPress Enter to continue...")
        clear_screen()

if __name__ == "__main__":
    clear_screen()
    main()

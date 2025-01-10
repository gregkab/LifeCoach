import requests
import datetime

API_URL = "http://localhost:8000/logs"

# Starting from today's date and moving backward
start_date = datetime.date(2024, 10, 25)

# Life-focused, diverse entries for each day
sample_data = [
    {
        "thoughts": "Set up a morning routine with meditation and journaling, reviewed monthly goals for personal growth.",
        "goals": "Complete a 15-minute meditation, write in journal, and review current progress on long-term goals.",
        "reflections": "Routine helped with clarity and focus. Monthly goals are on track, but need more consistent follow-through.",
        "goal_status": "in progress"
    },
    {
        "thoughts": "Explored new networking opportunities by reaching out to professionals on LinkedIn in my industry.",
        "goals": "Send connection requests with personalized messages to five people and schedule at least one informational interview.",
        "reflections": "Made three new connections and learned about trends in the industry; informational interview scheduled for next week.",
        "goal_status": "pending"
    },
    {
        "thoughts": "Read a book on financial literacy to improve budgeting skills and long-term financial planning.",
        "goals": "Finish reading one chapter and take notes on key concepts, especially around investments and budgeting.",
        "reflections": "Gained new insights on budgeting techniques and saving strategies; need to create a plan to implement these concepts.",
        "goal_status": "completed"
    },
    {
        "thoughts": "Experimented with a new productivity technique—time blocking—to improve focus and manage multiple tasks.",
        "goals": "Block out specific times for major tasks and stick to the schedule for the entire day.",
        "reflections": "Productivity was high during time blocks, but need to refine schedule for better flexibility.",
        "goal_status": "in progress"
    },
    {
        "thoughts": "Started a new workout routine focused on building strength and flexibility, targeting three sessions per week.",
        "goals": "Complete the first workout session with a focus on form and consistency.",
        "reflections": "Session went well; energy levels are high. Need to track progress over time to measure improvements.",
        "goal_status": "completed"
    },
    {
        "thoughts": "Tried a new meal-prepping technique to ensure healthier eating habits throughout the week.",
        "goals": "Plan and prepare meals for the next three days with balanced nutrients.",
        "reflections": "Prepared meals saved time and reduced stress. Planning to continue and refine meal choices.",
        "goal_status": "in progress"
    },
    {
        "thoughts": "Attended a workshop on public speaking to build confidence for upcoming presentations.",
        "goals": "Implement at least two tips from the workshop in daily conversations and observe any changes.",
        "reflections": "Applied tips on tone and eye contact; conversations felt more engaging. Need more practice.",
        "goal_status": "completed"
    }
]

# Adding logs for each day
for i in range(7):
    log_date = start_date - datetime.timedelta(days=i)
    data = {
        "date": log_date.isoformat(),
        "thoughts": sample_data[i]["thoughts"],
        "goals": sample_data[i]["goals"],
        "reflections": sample_data[i]["reflections"],
        "goal_status": sample_data[i]["goal_status"]
    }

    response = requests.post(API_URL, json=data)
    if response.status_code == 200:
        print(f"Log for {log_date} added successfully.")
    else:
        print(f"Failed to add log for {log_date}. Status code: {response.status_code}")

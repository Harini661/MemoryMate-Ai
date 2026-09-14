import json
import os
from datetime import datetime, date

REMINDER_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reminders.json")

def load_reminders():
    if os.path.exists(REMINDER_FILE):
        with open(REMINDER_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_reminder(task, due_date):
    reminders = load_reminders()
    new_reminder = {
        "task": task,
        "due_date": due_date,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    reminders.append(new_reminder)
    with open(REMINDER_FILE, "w", encoding="utf-8") as f:
        json.dump(reminders, f, indent=2, ensure_ascii=False)
    return new_reminder

def get_due_soon_reminders(days_threshold=2):
    reminders = load_reminders()
    today = date.today()
    due_soon = []
    for r in reminders:
        try:
            due = datetime.strptime(r["due_date"], "%Y-%m-%d").date()
            days_left = (due - today).days
            if 0 <= days_left <= days_threshold:
                r["days_left"] = days_left
                due_soon.append(r)
        except:
            continue
    return due_soon

def get_all_reminders():
    return load_reminders()
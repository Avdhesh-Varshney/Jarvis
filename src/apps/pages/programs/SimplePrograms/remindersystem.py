import time
import threading
from datetime import datetime

# Dictionary to store tasks and their times
tasks = {}

def add_task(task_name, task_time):
    tasks[task_name] = task_time
    print(f"Task '{task_name}' added for {task_time}.")

def task_reminder():
    while True:
        current_time = datetime.now().strftime("%H:%M")
        for task, task_time in list(tasks.items()):
            if task_time == current_time:
                print(f"Reminder: It's time to {task}!")
                del tasks[task]
        time.sleep(60)  # Check every minute

def main():
    # Start the reminder system in a separate thread
    reminder_thread = threading.Thread(target=task_reminder, daemon=True)
    reminder_thread.start()

    while True:
        task_name = input("Enter task name: ")
        task_time = input("Enter task time (HH:MM): ")
        add_task(task_name, task_time)

if __name__ == "__main__":
    main()

import streamlit as st

# Streamlit app code for a simple to-do list
def toDoList():
    st.title("📝 To-Do List Application")
    if 'tasks' not in st.session_state:
        st.session_state.tasks = []

    task_title = st.text_input("Task Title", "")
    task_description = st.text_area("Task Description", "")

    if st.button("Add Task"):
        if task_title:
            st.session_state.tasks.append({"title": task_title, "description": task_description, "completed": False})
            st.success(f"Task '{task_title}' added successfully!")
        else:
            st.error("Please provide a task title.")

    # Task filter: All, Completed, Pending
    filter_option = st.selectbox("Filter Tasks", ["All", "Completed", "Pending"])

    st.subheader("Your Tasks")
    filtered_tasks = []

    if filter_option == "Completed":
        filtered_tasks = [task for task in st.session_state.tasks if task["completed"]]
    elif filter_option == "Pending":
        filtered_tasks = [task for task in st.session_state.tasks if not task["completed"]]
    else:
        filtered_tasks = st.session_state.tasks

    for i, task in enumerate(filtered_tasks):
        col1, col2, col3 = st.columns([0.1, 0.6, 0.3])
        with col1:
            task_done = st.checkbox("", value=task["completed"], key=f"task_done_{i}")
        with col2:
            st.write(f"**{task['title']}** - {task['description']}")
        with col3:
            if st.button("Delete", key=f"delete_{i}"):
                st.session_state.tasks.remove(task)
                st.experimental_rerun()

        # Mark tasks as completed
        if task_done:
            st.session_state.tasks[i]["completed"] = True

    # Task progress
    total_tasks = len(st.session_state.tasks)
    completed_tasks = sum(1 for task in st.session_state.tasks if task["completed"])

    if total_tasks > 0:
        st.progress(completed_tasks / total_tasks)
        st.write(f"Progress: {completed_tasks}/{total_tasks} tasks completed.")



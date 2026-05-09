import streamlit as st
import pandas as pd
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="DevPulse | Project Tracker", layout="wide")

# --- CUSTOM CSS FOR MINIMAL LOOK ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

# --- SIDEBAR: ADD NEW TASK ---
with st.sidebar:
    st.header("📌 New Task")
    task_name = st.text_input("Task Title", placeholder="e.g., Setup MongoDB Pipeline")
    priority = st.select_slider("Priority", options=["Low", "Medium", "High"])
    category = st.selectbox("Category", ["Frontend", "Backend", "Data Engineering", "Documentation"])
    
    if st.button("Add Task"):
        if task_name:
            new_task = {
                "id": len(st.session_state.tasks) + 1,
                "name": task_name,
                "priority": priority,
                "category": category,
                "status": "Backlog",
                "date": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            st.session_state.tasks.append(new_task)
            st.toast(f"Added: {task_name}")
        else:
            st.error("Please name the task.")

# --- MAIN DASHBOARD ---
st.title("🚀 DevPulse Project Board")
st.write(f"Logged in as **Rawan Ayman Saber**") #

# Quick Metrics
cols = st.columns(3)
cols[0].metric("Total Tasks", len(st.session_state.tasks))
cols[1].metric("In Progress", len([t for t in st.session_state.tasks if t['status'] == "Doing"]))
cols[2].metric("Completed", len([t for t in st.session_state.tasks if t['status'] == "Done"]))

st.divider()

# --- KANBAN BOARD COLUMNS ---
c1, c2, c3 = st.columns(3)

sections = {
    "Backlog": c1,
    "Doing": c2,
    "Done": c3
}

for status, col in sections.items():
    with col:
        st.subheader(f" {status}")
        filtered_tasks = [t for t in st.session_state.tasks if t['status'] == status]
        
        for task in filtered_tasks:
            with st.expander(f"{task['name']}"):
                st.caption(f"Category: {task['category']} | {task['date']}")
                st.write(f"Priority: **{task['priority']}**")
                
                # Move Logic
                if status == "Backlog":
                    if st.button(f"Start →", key=f"start_{task['id']}"):
                        task['status'] = "Doing"
                        st.rerun()
                elif status == "Doing":
                    if st.button(f"Finish ✔", key=f"done_{task['id']}"):
                        task['status'] = "Done"
                        st.rerun()
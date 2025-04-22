import streamlit as st
import pandas as pd
from st_aggrid import GridOptionsBuilder, AgGrid

# Initialize session state for tasks and messages
if 'tasks' not in st.session_state:
    st.session_state.tasks = {'To Do': [], 'In Progress': [], 'Done': []}
if 'messages' not in st.session_state:
    st.session_state.messages = []

# User authentication
if 'username' not in st.session_state:
    st.session_state.username = None

def login():
    st.session_state.username = st.text_input("Username", "")
    if st.session_state.username:
        st.success(f"Welcome, {st.session_state.username}!")

def logout():
    st.session_state.username = None
    st.session_state.tasks = {'To Do': [], 'In Progress': [], 'Done': []}
    st.session_state.messages = []
    st.success("You have been logged out.")

# Streamlit layout
st.title("Remote Team Collaboration Tool")

if st.session_state.username is None:
    login()
else:
    st.sidebar.button("Logout", on_click=logout)

    # Task management
    st.subheader("Add Task")
    task = st.text_input("Enter a new task:")
    status = st.selectbox("Select Status", ["To Do", "In Progress", "Done"])
    
    if st.button("Add Task"):
        if task:
            st.session_state.tasks[status].append(task)
            st.success("Task added!")
        else:
            st.warning("Please enter a task.")

    # Kanban board display
    st.subheader("Kanban Board")
    for column in st.session_state.tasks:
        st.write(f"### {column}")
        tasks = st.session_state.tasks[column]

        # Create a DataFrame for AgGrid
        df = pd.DataFrame(tasks, columns=["Task"])
        df['Status'] = column  # Add a status column for filtering

        # Display tasks in Kanban style with AgGrid
        grid_options = GridOptionsBuilder.from_dataframe(df)
        grid_options.configure_pagination(paginationPageSize=5)
        grid_options.configure_default_column(editable=True)
        grid_options.configure_column("Task", header_name="Task", cell_editor="text")
        grid_options.configure_column("Status", header_name="Status", cell_editor="text", editable=False)

        AgGrid(df, gridOptions=grid_options, enable_enterprise_modules=True)

    # Messaging feature
    st.subheader("Messaging")
    message = st.text_input("Enter your message:")
    if st.button("Send Message"):
        if message:
            st.session_state.messages.append(f"{st.session_state.username}: {message}")
            st.success("Message sent!")
        else:
            st.warning("Please enter a message.")

    # Display messages
    st.write("### Messages")
    if st.session_state.messages:
        for msg in st.session_state.messages:
            st.write(msg)
    else:
        st.write("No messages yet.")
import streamlit as st
import json
from typing import List
from pathlib import Path
from st_pages import Page, show_pages, add_page_title

# Optional -- adds the title and icon to the current page
add_page_title()

# Specify what pages should be shown in the sidebar, and what their titles and icons
# should be
show_pages(
    [
        Page("Admin_Section.py", "Login", "🏠"),
        Page("pages/Instructor_Quiz_Config.py", "Page 2", ":Question_Generation:"),
        Page("pages/DocuBOT.py", "Page 3", ":Chat_with_Books:"),
        Page("pages/DocuBOT_Quiz_Mode.py.py", "Page 4", ":Chat_Quiz:"),
        Page("pages/Admin_Controls.py", "Page 5", ":Admin_Controls:"),

    ]
)

DB_FILE = "db.json"


class User:
    def __init__(self, username, password, user_type, instructor=None, assignments=None):
        self.username = username
        self.password = password
        self.user_type = user_type
        self.instructor = instructor
        self.assignments = assignments if assignments else []

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "user_type": self.user_type,
            "instructor": self.instructor,
            "assignments": self.assignments,
        }


def load_users() -> List[User]:
    if Path(DB_FILE).is_file():
        with open(DB_FILE, "r") as f:
            users_data = json.load(f)
        return [User(**user_data) for user_data in users_data]
    else:
        return []


def save_users(users: List[User]):
    users_data = [user.to_dict() for user in users]
    with open(DB_FILE, "w") as f:
        json.dump(users_data, f)



def main():
    st.title("Login or Register")

    users = load_users()

    if "username" not in st.session_state:
        username = st.text_input("Username", value="learner1")
        password = st.text_input("Password",value="password3" ,type="password")

        if st.button("Login"):
            user = [user for user in users if user.username == username and user.password == password]
            if user:
                user = user[0]
                st.session_state['username'] = user.username
                st.session_state['user_type'] = user.user_type
                st.write(f"Logged in as {user.username} ({user.user_type}).")
            else:
                st.write("Invalid username or password.")
    else:
        user = [u for u in users if u.username == st.session_state['username']][0]
        if user.user_type == "instructor":
            st.write(f"Welcome, {user.username}! You are an instructor.")
            st.write("List of your students:")
            students = [u for u in users if u.user_type == "learner" and u.instructor == user.username]
            for student in students:
                st.write(student.username)
        else:
            st.write(f"Welcome, {user.username}! You are a learner.")
            st.write(f"Your instructor is: {user.instructor}")
            st.write("Your assignments:")
            for assignment in user.assignments:
                st.write(assignment)
                

    st.title("Register")
    user_type = st.selectbox("User Type", ["learner", "instructor"])
    if user_type == "learner":
        instructors = [user for user in users if user.user_type == "instructor"]
        instructor_usernames = [instructor.username for instructor in instructors]
        selected_instructor = st.selectbox("Select an Instructor", instructor_usernames)

    if st.button("Register"):
        if user_type == "instructor":
            new_user = User(username, password, user_type)
        else:
            new_user = User(username, password, user_type, selected_instructor)

        users.append(new_user)
        save_users(users)
        st.write(f"User {username} registered successfully as a {user_type}.")
 
    if st.button("Logout"):
        keys_to_remove = list(st.session_state.keys())  # Get a list of all session state keys
        for key in keys_to_remove:
            st.session_state.pop(key, None)  # Remove each key from the session state
        st.write("Logged out successfully.")

if __name__ == "__main__":
    main()


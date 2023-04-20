import streamlit as st
import json
from typing import List
from pathlib import Path
from st_pages import Page, Section, show_pages, add_page_title


DB_FILE = "db.json"

show_pages(
    [
        Page("Admin_Section.py", "Home", "🏠"),
        Page("pages/Login_new.py", "Login / Signup", "🎈️"),
        Page("pages/Admin_Controls.py", "Admin Control", "💪"),
        Page("pages/DocuBOT.py", "DocuBOT", "💪"),
    ]
)


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
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            user = [user for user in users if user.username ==
                    username and user.password == password]
            if user:
                user = user[0]
                st.session_state['username'] = user.username
                st.session_state['user_type'] = user.user_type
                st.write(f"Logged in as {user.username} ({user.user_type}).")
            else:
                st.write("Invalid username or password.")
    else:
        user = [u for u in users if u.username ==
                st.session_state['username']][0]
        if user.user_type == "instructor":
            st.write(f"Welcome, {user.username}! You are an instructor.")
            st.write("List of your students:")
            students = [u for u in users if u.user_type ==
                        "learner" and u.instructor == user.username]
            for student in students:
                st.write(student.username)
        else:
            st.write(f"Welcome, {user.username}! You are a learner.")
            st.write(f"Your instructor is: {user.instructor}")
            # st.write("Your assignments:")
            # for assignment in user.assignments:
            #     st.write(assignment)

    st.title("Register")
    user_type = st.selectbox("User Type", ["learner", "instructor"])
    if user_type == "learner":
        instructors = [
            user for user in users if user.user_type == "instructor"]
        instructor_usernames = [
            instructor.username for instructor in instructors]
        selected_instructor = st.selectbox(
            "Select an Instructor", instructor_usernames)

    if st.button("Register"):
        if user_type == "instructor":
            new_user = User(username, password, user_type)
        else:
            new_user = User(username, password, user_type, selected_instructor)

        users.append(new_user)
        save_users(users)
        st.write(f"User {username} registered successfully as a {user_type}.")

    if st.button("Logout"):
        st.session_state.pop('username', None)
        st.session_state.pop('user_type', None)
        st.write("Logged out successfully.")
        show_pages(
            [
                Page("Admin_Section.py", "Home", "🏠"),
                Page("pages/Login_new.py", "Login / Signup", "🎈️"),
                Page("pages/Admin_Controls.py", "Admin Control", "💪"),
            ]
        )


if __name__ == "__main__":
    main()

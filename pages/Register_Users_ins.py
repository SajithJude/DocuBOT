import streamlit as st
import json
from typing import List
from pathlib import Path
from st_pages import Page, Section, show_pages, add_page_title

st.set_page_config(page_title="DocuBOT", page_icon=None,
                   layout="wide")


def set_style():
    st.markdown(
        f"""
        <style>
            .reportview-container .main .block-container{{
                max-width: {1500}px;
                padding-top: {5}rem;
                padding-right: {2}rem;
                padding-left: {2}rem;
                padding-bottom: {10}rem;
            }}
            .reportview-container .main {{
                color: {'#333333'};
                background-color: {'#F5F5F5'};
            }}
        </style>
        """,
        unsafe_allow_html=True,
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
    set_style()

    users = load_users()

    container = st.container()

    with container:

        st.subheader("Register New User")
        user_type = "learner"
        instructors = [
            user for user in users if user.user_type == "instructor"]
        instructor_usernames = [
            instructor.username for instructor in instructors]
        selected_instructor = st.selectbox(
            "Assign an Instructor", instructor_usernames)
        username_reg = st.text_input("Username (Learner)")
        password_reg = st.text_input(
            "Password (Learner)", type="password")

        if st.button("Register"):
            if not username_reg or not password_reg:
                st.write("Please enter a username and password.")
            else:
                new_user = User(username_reg, password_reg,
                                user_type, instructor=selected_instructor)
                users.append(new_user)
                save_users(users)
                st.success(
                    f"User {username_reg} registered successfully as a {user_type}.")


if __name__ == "__main__":
    main()

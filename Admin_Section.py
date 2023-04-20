import streamlit as st
import json
from typing import List
from pathlib import Path
from st_pages import Page, Section, show_pages, add_page_title, hide_pages

st.set_page_config(page_title="DocuBOT", page_icon=None,
                   layout="wide")
show_pages(
    [
        Page("Admin_Section.py", "Home", "🏠"),

    ]
)


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
    if "username" not in st.session_state:
        container = st.container()

        with container:
            tab1, tab2 = st.tabs(["Login", "Register as a Learner"])

            with tab1:
                st.subheader("Login")
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")

                if st.button("Login"):
                    user = [user for user in users if user.username ==
                            username and user.password == password]
                    if user:
                        user = user[0]
                        st.session_state['username'] = user.username
                        st.session_state['user_type'] = user.user_type
                        st.success(
                            f"Logged in as {user.username} ({user.user_type}).")

                    else:
                        st.write("Invalid username or password.")
                    st.experimental_rerun()
            with tab2:
                st.subheader("Register as a Learner")
                user_type = "learner"
                username_reg = st.text_input("Username (Learner)")
                password_reg = st.text_input(
                    "Password (Learner)", type="password")
                if st.button("Register"):
                    if not username_reg or not password_reg:
                        st.write("Please enter a username and password.")
                    else:
                        new_user = User(username_reg, password_reg, user_type)
                        users.append(new_user)
                        save_users(users)
                        st.success(
                            f"User {username_reg} registered successfully as a {user_type}.")

        # if st.button("Logout"):
        #     # Get a list of all session state keys
        #     keys_to_remove = list(st.session_state.keys())
        #     for key in keys_to_remove:
        #         # Remove each key from the session state
        #         st.session_state.pop(key, None)
        #     st.write("Logged out successfully.")
    else:
        st.write("Logged in as "+str(st.session_state['username']))


if __name__ == "__main__":
    main()
    if "username" in st.session_state:
        Logout = st.button("Logout")
        pass
        if Logout:
            # Get a list of all session state keys
            keys_to_remove = list(st.session_state.keys())
            for key in keys_to_remove:
                # Remove each key from the session state
                st.session_state.pop(key, None)
            st.write("Logged out successfully.")
            st.experimental_rerun()

    if "username" in st.session_state:
        users = load_users()
        user = [u for u in users if u.username ==
                st.session_state['username']][0]

        if user.user_type == "instructor":
            show_pages([
                Page("Admin_Section.py", "Home", "🏠"),
                Page("pages/Instructor_Quiz_Config.py",
                     "Question_Generation", " 📕"),
                Page("pages/DocuBOT.py",  "DocuBOT", ":books:"),
                Page("pages/instructor_controls.py",
                     "Instructor Controls", "🧑🏻‍🏫")
            ])

        elif user.user_type == "learner":
            show_pages([
                Page("Admin_Section.py", "Home", "🏠"),
                Page("pages/DocuBOT_Quiz_Mode.py",  "DocuBOT_Quiz_Mode", "📝"),
                Page("pages/DocuBOT.py",  "DocuBOT", ":books:")
            ])

        elif user.user_type == "superadmin":
            show_pages([
                Page("Admin_Section.py", "Home", "🏠"),
                Page("pages/Register_Users_super.py",
                     "Register New Users"),
                Page("pages/DocuBOT.py",  "DocuBOT", ":books:"),
                Page("pages/Admin_Controls.py",  "Admin_Controls")
            ])
        elif user.user_type == "admin":
            show_pages([
                Page("Admin_Section.py", "Home", "🏠"),
                Page("pages/Register_Users_admin.py",
                     "Register New Users"),
                Page("pages/DocuBOT.py",  "DocuBOT", ":books:"),
                Page("pages/Admin_Controls.py",  "Admin_Controls")
            ])
        else:

            hide_pages([

                Page("pages/My_Profile.py", "My Profile"),
                Page("pages/Register_Users_super.py",
                     "Register New Users"),
                Page("pages/DocuBOT_Quiz_Mode.py",  "DocuBOT_Quiz_Mode"),
                Page("pages/DocuBOT.py",  "DocuBOT", ":books:"),
                Page("pages/Admin_Controls.py",  "Admin_Controls")
            ])
            show_pages([
                Page("Admin_Section.py", "Home", "🏠")
            ])

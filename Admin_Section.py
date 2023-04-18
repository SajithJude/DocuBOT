# import streamlit as st
# import json
# from typing import List
# from pathlib import Path

# DB_FILE = "db.json"


# class User:
#     def __init__(self, username, password, user_type, instructor=None, assignments=None):
#         self.username = username
#         self.password = password
#         self.user_type = user_type
#         self.instructor = instructor
#         self.assignments = assignments if assignments else []

#     def to_dict(self):
#         return {
#             "username": self.username,
#             "password": self.password,
#             "user_type": self.user_type,
#             "instructor": self.instructor,
#             "assignments": self.assignments,
#         }


# def load_users() -> List[User]:
#     if Path(DB_FILE).is_file():
#         with open(DB_FILE, "r") as f:
#             users_data = json.load(f)
#         return [User(**user_data) for user_data in users_data]
#     else:
#         return []


# def save_users(users: List[User]):
#     users_data = [user.to_dict() for user in users]
#     with open(DB_FILE, "w") as f:
#         json.dump(users_data, f)


# def main():
#     st.title("Login or Register")

#     users = load_users()

#     if "username" not in st.session_state:
#         username = st.text_input("Username")
#         password = st.text_input("Password", type="password")

#         if st.button("Login"):
#             user = [user for user in users if user.username ==
#                     username and user.password == password]
#             if user:
#                 user = user[0]
#                 st.session_state['username'] = user.username
#                 st.session_state['user_type'] = user.user_type
#                 st.write(f"Logged in as {user.username} ({user.user_type}).")
#             else:
#                 st.write("Invalid username or password.")
#     else:
#         user = [u for u in users if u.username ==
#                 st.session_state['username']][0]
#         if user.user_type == "instructor":
#             st.write(f"Welcome, {user.username}! You are an instructor.")
#             st.write("List of your students:")
#             students = [u for u in users if u.user_type ==
#                         "learner" and u.instructor == user.username]
#             for student in students:
#                 st.write(student.username)
#         else:
#             st.write(f"Welcome, {user.username}! You are a learner.")
#             st.write(f"Your instructor is: {user.instructor}")
#             # st.write("Your assignments:")
#             # for assignment in user.assignments:
#             #     st.write(assignment)

#     st.title("Register")
#     user_type = st.selectbox("User Type", ["learner", "instructor"])
#     if user_type == "learner":
#         instructors = [
#             user for user in users if user.user_type == "instructor"]
#         instructor_usernames = [
#             instructor.username for instructor in instructors]
#         selected_instructor = st.selectbox(
#             "Select an Instructor", instructor_usernames)

#     if st.button("Register"):
#         if user_type == "instructor":
#             new_user = User(username, password, user_type)
#         else:
#             new_user = User(username, password, user_type, selected_instructor)

#         users.append(new_user)
#         save_users(users)
#         st.write(f"User {username} registered successfully as a {user_type}.")

#     if st.button("Logout"):
#         st.session_state.pop('username', None)
#         st.session_state.pop('user_type', None)
#         st.write("Logged out successfully.")


# if __name__ == "__main__":
#     main()

import streamlit as st
import json
from typing import List
from pathlib import Path


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
        tab1, tab2 = st.tabs(["Login", "Register"])

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
                    st.write(
                        f"Logged in as {user.username} ({user.user_type}).")
                else:
                    st.write("Invalid username or password.")

        with tab2:
            st.subheader("Register")
            user_type = st.selectbox(
                "User Type", ["learner", "instructor"])
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

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
                    new_user = User(
                        username, password, user_type, selected_instructor)

                users.append(new_user)
                save_users(users)
                st.write(
                    f"User {username} registered successfully as a {user_type}.")

    if st.button("Logout"):
        st.session_state.pop('username', None)
        st.session_state.pop

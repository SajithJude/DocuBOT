import streamlit as st
import json
from typing import List
from pathlib import Path

DB_FILE = "db.json"


class User:
    # (same as before)

# (same as before: load_users, save_users)


def main():
    st.title("Login or Register")

    users = load_users()

    if "username" not in st.session_state:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

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

    # (same as before: registration)

    if st.button("Logout"):
        st.session_state.pop('username', None)
        st.session_state.pop('user_type', None)
        st.write("Logged out successfully.")


if __name__ == "__main__":
    main()

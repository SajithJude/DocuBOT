import streamlit as st
import json
from typing import List
from pathlib import Path
from st_pages import Page, Section, show_pages, add_page_title


def main():

    st.title("My Profile")

    if "username" in st.session_state:

        username = st.session_state['username']
        password = st.session_state['password']
        user_type = st.session_state['user_type']

    st.write("User Name")
    st.write(username)

    st.write('')

    st.write("User Type")
    st.write(user_type)

    if st.sidebar.button("Logout"):
        # Get a list of all session state keys
        keys_to_remove = list(st.session_state.keys())
        for key in keys_to_remove:
            # Remove each key from the session state
            st.session_state.pop(key, None)
        st.write("Logged out successfully.")
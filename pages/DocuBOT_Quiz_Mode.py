import streamlit as st
import json
from typing import List
from pathlib import Path

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


st.set_page_config(
    page_title="DocuBOT QuizMode",
    page_icon=":robot:"
)

st.header("DocuBOT QuizMode")

users = load_users()

if "username" in st.session_state:
    user = [u for u in users if u.username == st.session_state['username']][0]
    if user.user_type == "learner":
        questions = user.assignments

        if 'past' not in st.session_state:
            st.session_state['past'] = []

        if 'current_question' not in st.session_state:
            st.session_state['current_question'] = 0

        def get_text():
            input_text = st.text_input("You: ", "", key="input")
            submit_button = st.button("Submit Answer", key="submit_button")
            return input_text, submit_button

        if st.session_state['current_question'] < len(questions):
            current_question = questions[st.session_state['current_question']]
            st.write(f"Bot: {current_question['question']}")
            user_input, submit_button = get_text()

            if submit_button and user_input:
                st.session_state['past'].append(user_input)
                st.session_state['current_question'] += 1
                st.text_input("You: ", value="", key="input")  # Reset the text input field

        else:
            responses = []
            for i, question in enumerate(questions):
                response = {
                    "question": question['question'],
                    "response": st.session_state['past'][i]
                }
                responses.append(response)

            user.assignments = responses
            save_users(users)

            st.write("Thank you for answering all the questions. Your responses have been saved.")
            st.download_button(
                label="Download Responses",
                data=json.dumps(responses),
                file_name="responses.json",
                mime="application/json"
            )
else:
    st.info("Please Login or Register")


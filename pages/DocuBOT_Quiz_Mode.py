import streamlit as streamlit
from streamlit_chat import message
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


streamlit.set_page_config(
    page_title="DocuBOT QuizMode",
    page_icon=":robot:"
)

streamlit.header("DocuBOT QuizMode")

users = load_users()

if "username" in streamlit.session_state:
    user = [u for u in users if u.username == streamlit.session_state['username']][0]
    if user.user_type == "learner":
        questions = user.assignments
        # streamlit.write(questions)
        if 'generated' not in streamlit.session_state:
            streamlit.session_state['generated'] = []

        if 'past' not in streamlit.session_state:
            streamlit.session_state['past'] = []
            
        if 'current_question' not in streamlit.session_state:
            streamlit.session_state['current_question'] = 1

        def get_text():
            input_text = streamlit.text_input("You: ","", key="input")
            return input_text 

        if streamlit.session_state['current_question'] < len(questions):
            current_question = questions[streamlit.session_state['current_question']]
            message(current_question['question'], is_user=False, key=str(streamlit.session_state['current_question']))
            user_input = get_text()

            if user_input:
                streamlit.session_state['past'].append(user_input)
                streamlit.session_state['current_question'] += 1

            streamlit.sidebar.header("Conversation History")
            for i, question in enumerate(questions):
                if i < streamlit.session_state['current_question']:
                    streamlit.sidebar.write(question['question'])
                    streamlit.sidebar.write("You: " + streamlit.session_state['past'][i])

        else:
            responses = []
            for i, question in enumerate(questions):
                response = {
                    "question": question['question'],
                    "response": streamlit.session_state['past'][i]
                }
                responses.append(response)
            
            # with open("responses.json", "w") as outfile:
            #     json.dump(responses, outfile)
                user.assignments[streamlit.session_state['current_question'] - 1]['responses'] = responses
                save_users(users)

            message("Thank you for answering all the questions. Your responses have been saved.", is_user=False)
            streamlit.sidebar.write("Thank you for answering all the questions. Your responses have been saved.")

            streamlit.sidebar.download_button(
                label="Download Responses",
                data=json.dumps(responses),
                file_name="responses.json",
                mime="application/json"
            )

    if streamlit.session_state['generated']:
        for i in range(len(streamlit.session_state['generated'])-1, -1, -1):
            message(streamlit.session_state["generated"][i], key=str(i))
            message(streamlit.session_state['past'][i], is_user=True, key=str(i) + '_user')
            streamlit.sidebar.write("Bot: ", streamlit.session_state["generated"][i])

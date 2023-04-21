import streamlit as st
import openai
import os
import json
import base64
from typing import List
# import streamlit as st
from pathlib import Path
import json

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

    st.title("Assignment Submission")
    users = load_users()

    # Check if the user is logged in and is an instructor
    if "username" in st.session_state and st.session_state["user_type"] == "instructor":
        instructor = [u for u in users if u.username ==
                      st.session_state['username']][0]

        try:
            responses = st.session_state.json_output
        except AttributeError:
            st.info("Generate questions to get started")

        # Choose a student to assign the responses
        students = [u for u in users if u.user_type ==
                    "learner" and u.instructor == instructor.username]
        student_usernames = [s.username for s in students]
        selected_student = st.selectbox(
            "Select the student to assign the responses", student_usernames)

        if st.button("Assign Assignment"):
            # Find the selected student and update their assignments
            for student in students:
                if student.username == selected_student:
                    student.assignments.append(
                        {"topic": st.session_state['topic'], "responses": responses})
                    break

            instructor.assignments.append(
                {"topic": st.session_state['topic'], "responses": responses})

            # Save the updated users to the db.json file
            save_users(users)
            st.success(f"Responses assigned to {selected_student}.")
    else:
        st.warning("Please log in as an instructor to assign responses.")


if __name__ == "__main__":

    users = load_users()
    main()

    if "username" in st.session_state:
        user = [u for u in users if u.username ==
                st.session_state['username']][0]
        if user.user_type == "instructor":

            openai.api_key = os.getenv("OPENAI_API_KEY")

            st.subheader("Question & Answer Generation Admin section")

            form = """
            [
            {
                "question": "Question here?",
                "answer": "Answer here.",
                "Question": "Question here?"
            },
            { 
                "question": "Question here?",
                "answer": "Answer here.",
                "Question": "Question here?"
            }
            ]
            """

            topic = st.text_input("Enter topic here")

            num_quest = st.slider('Number of questions to generate', 0, 10, 1)
            result = st.button("Submit")

            if result:
                st.session_state['topic'] = topic
                prompt = f"generate {num_quest} essay type questions with answers on the topic of {topic}, with the all the possible correct comprehensive answers, show the output in following json list format:\n {form}."
                response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=prompt,
                    temperature=0.56,
                    max_tokens=2100,
                    top_p=1,
                    frequency_penalty=0.35,
                    presence_penalty=0
                )
                output = response.choices[0].text.strip()
                json_output = json.loads(output)
                # st.write(json_output)
                # Initialization

            # Session State also supports attribute based syntax
                if 'json_output' not in st.session_state:
                    st.session_state.json_output = json_output
            # except AttributeError:

            try:
                st.subheader("Refining section by subject matter expert")
                # Display the JSON output as editable text_input fields
                for i, item in enumerate(st.session_state.json_output):
                    st.write(f"question {i+1}")
                    question = st.text_input("question", item["question"])
                    answer = st.text_area("answer", item["answer"])

                    # Update the JSON output with the edited fields
                    st.session_state.json_output[i]["Question"] = question
                    st.session_state.json_output[i]["answer"] = answer

                # Display a download button to download the edited version
                edited_json = json.dumps(
                    st.session_state.json_output, indent=2)
            except AttributeError:
                st.warning(
                    "Type a topic and generate some questions to refine them")

    else:
        st.info("Please Login or Register")

        # openai.api_key = os.getenv("OPENAI_API_KEY")

        # st.subheader("Question & Answer Generation Admin section")

        # form = """
        # [
        #   {
        #     "question": "Question here?",
        #     "answer": "Answer here.",
        #     "Question": "Question here?"
        #   },
        #   {
        #     "question": "Question here?",
        #     "answer": "Answer here.",
        #     "Question": "Question here?"
        #   }
        # ]
        # """

        # topic = st.text_input("Enter topic here")
        # num_quest = st.slider('Number of questions to generate', 0, 10, 1)
        # result = st.button("Submit")

        # if result:
        #     prompt = f"generate {num_quest} essay type questions with answers on the topic of {topic}, with the all the possible correct comprehensive answers, show the output in following json list format:\n {form}."
        #     response = openai.Completion.create(
        #         model="text-davinci-003",
        #         prompt=prompt,
        #         temperature=0.56,
        #         max_tokens=2100,
        #         top_p=1,
        #         frequency_penalty=0.35,
        #         presence_penalty=0
        #     )
        #     output = response.choices[0].text.strip()
        #     json_output = json.loads(output)
        #     # st.write(json_output)
        #     # Initialization

        # # Session State also supports attribute based syntax
        #     if 'json_output' not in st.session_state:
        #         st.session_state.json_output = json_output
        # # except AttributeError:

        # try:
        #     st.subheader("Refining section by subject matter expert")
        #         # Display the JSON output as editable text_input fields
        #     for i, item in enumerate(st.session_state.json_output):
        #         st.write(f"question {i+1}")
        #         question = st.text_input("question", item["question"])
        #         answer = st.text_area("answer", item["answer"])

        #         # Update the JSON output with the edited fields
        #         st.session_state.json_output[i]["Question"] = question
        #         st.session_state.json_output[i]["answer"] = answer

        #     # Display a download button to download the edited version
        #     edited_json = json.dumps(st.session_state.json_output, indent=2)
        #     b64 = base64.b64encode(edited_json.encode()).decode()
        #     href = f'<a href="data:file/json;base64,{b64}" download="{topic}.json">Download edited JSON file</a>'
        #     st.markdown(href, unsafe_allow_html=True)
        # except AttributeError:
        #     st.warning("Type a topic and generate some questions to refine them")

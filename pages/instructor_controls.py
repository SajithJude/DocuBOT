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

openai.api_key = os.getenv("OPENAI_API_KEY")


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


def view_responses(users):
    instructor = [u for u in users if u.username ==
                  st.session_state['username']][0]
    students = [u for u in users if u.user_type ==
                "learner" and u.instructor == instructor.username]
    student_usernames = [s.username for s in students]

    selected_student = st.selectbox(
        "Select a student to view their responses", student_usernames)
    selected_student_obj = [
        s for s in students if s.username == selected_student][0]

    topics = list(set([a["topic"] for a in selected_student_obj.assignments]))
    selected_topic = st.selectbox("Select a topic to view responses", topics)
    grade = st.button("grade")
    col1, col2 = st.columns(2)
    # if col1.button("View Responses"):
    student_ans = []
    real_ans = []

    for assignment in selected_student_obj.assignments:
        if assignment["topic"] == selected_topic:
            for i, response in enumerate(assignment["responses"]):
                col1.write(f"Question {i+1}: {response['question']}")
                col1.write(f"Student's Answer: {response['answer']}")
                student_ans.append(response['answer'])
            break

    # if col2.button("Compare Responses"):
    for assignment in instructor.assignments:
        if assignment["topic"] == selected_topic:
            for i, response in enumerate(assignment["responses"]):
                col2.write(f"Question {i+1}: {response['question']}")
                col2.write(f"Instructor's Answer: {response['answer']}")
                real_ans.append(response['answer'])
            break

    if grade:
        # st.write(student_ans,real_ans)
        prompt = f"compare the following list of answers given by a student with the actuall answer, if the students answer is contextually similar with the actual answer even without being exactly the same consider the student answer correct,  and generate a percentage for each answer on how much they match with the actual answer and also generate feed back for the student on the areas he needs to focus on learning\n Students Answers : {str(student_ans)}\n Actual Answers :  {str(real_ans)}"
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
        st.write(output)


def main():

    st.title("Assignment Submission")
    users = load_users()

    # Check if the user is logged in and is an instructor
    if "username" in st.session_state and st.session_state["user_type"] == "instructor":
        view_responses(users)
    else:
        st.warning("Please log in as an instructor to view student responses.")


if __name__ == "__main__":

    # users = load_users()
    main()

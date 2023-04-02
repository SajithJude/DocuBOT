import streamlit as st 
import openai
import os
import json
from streamlit import caching
import base64
from sessionstate import get

openai.api_key = os.getenv("OPENAI_API_KEY")

DATA_DIR = "data"
# Get a list of available index files in the data directory
index_filenames = [f for f in os.listdir(DATA_DIR) if f.endswith(".json")]

session = get(json_output=[], edited_json="")
book = st.selectbox("Select a Book ", index_filenames)
topic = st.text_input("Enter topic here")
# subtopic = st.text_input("Enter subtopic here")
num_quest = st.slider('Number of questions to generate', 0, 10, 1)
result = st.button("Submit")

if result:
    prompt = f"generate {num_quest} essay type questions with answers on the topic of {topic}, with the correct answers and marking criteria with marks per criteria, show the output in json list format."
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

    # Store the JSON output in the session state
    session.json_output = json_output

# Display the JSON output as editable text_input fields
for i, item in enumerate(session.json_output):
    st.write(f"Question {i+1}")
    question = st.text_input("Question", item["Question"])
    answer = st.text_input("Answer", item["Answer"])
    marking_criteria = item["Marking Criteria"]
    st.write("Marking Criteria")
    for j, criterion in enumerate(marking_criteria):
        if "Correct Answer" in criterion:
            marks = st.number_input(f"Correct Answer {criterion['Correct Answer']} Marks", value=criterion["Marks"])
            marking_criteria[j]["Marks"] = marks
        elif "Incorrect Answer" in criterion:
            marks = st.number_input(f"Incorrect Answer {criterion['Incorrect Answer']} Marks", value=criterion["Marks"])
            marking_criteria[j]["Marks"] = marks

    # Update the JSON output with the edited fields
    session.json_output[i]["Question"] = question
    session.json_output[i]["Answer"] = answer
    session.json_output[i]["Marking Criteria"] = marking_criteria

# Display a download button to download the edited version
if session.json_output:
    edited_json = json.dumps(session.json_output, indent=2)
    session.edited_json = edited_json
    b64 = base64.b64encode(edited_json.encode()).decode()
    href = f'<a href="data:file/json;base64,{b64}" download="{topic}.json">Download edited JSON file</a>'
    st.markdown(href, unsafe_allow_html=True)

# Clear the cache if the book is changed
if session.json_output and book != index_filenames:
    session.json_output = []
    session.edited_json = ""
    caching.clear_cache()

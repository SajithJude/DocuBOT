import streamlit as st 
import openai
import os
import json
import base64

openai.api_key = os.getenv("OPENAI_API_KEY")

# DATA_DIR = "data"
# # Get a list of available index files in the data directory
# index_filenames = [f for f in os.listdir(DATA_DIR) if f.endswith(".json")]

# book = st.selectbox("Select a Book ", index_filenames)
topic = st.text_input("Enter topic here")
# subtopic = st.text_input("Enter subtopic here")
num_quest = st.slider('Number of questions to generate', 0, 10, 1)
result = st.button("Submit")

if result:
    prompt = f"generate {num_quest} essay type questions with answers on the topic of {topic}, with the all the possible correct comprehensive answers, show the output in json list format."
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
    st.write(json_output)
    # Initialization

# Session State also supports attribute based syntax
    if 'json_output' not in st.session_state:
        st.session_state.json_output = json_output

    # Display the JSON output as editable text_input fields
for i, item in enumerate(st.session_state.json_output):
    st.write(f"question {i+1}")
    question = st.text_input("question", item["question"])
    answer = st.text_area("answer", item["answer"])
    # marking_criteria = item["Marking Criteria"]
    # st.write("Marking Criteria")
    # for j, criterion in enumerate(marking_criteria):
    #     if "Correct answer" in criterion:
    #         marks = st.number_input(f"Correct answer {criterion['Correct answer']} Marks", value=criterion["Marks"])
    #         marking_criteria[j]["Marks"] = marks
    #     elif "Incorrect answer" in criterion:
    #         marks = st.number_input(f"Incorrect answer {criterion['Incorrect answer']} Marks", value=criterion["Marks"])
    #         marking_criteria[j]["Marks"] = marks

    # Update the JSON output with the edited fields
    st.session_state.json_output[i]["Question"] = question
    st.session_state.json_output[i]["answer"] = answer
    # st.session_state.json_output[i]["Marking Criteria"] = marking_criteria

# Display a download button to download the edited version
edited_json = json.dumps(st.session_state.json_output, indent=2)
b64 = base64.b64encode(edited_json.encode()).decode()
href = f'<a href="data:file/json;base64,{b64}" download="{topic}.json">Download edited JSON file</a>'
st.markdown(href, unsafe_allow_html=True)

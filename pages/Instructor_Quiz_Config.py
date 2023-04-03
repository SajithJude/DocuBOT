import streamlit as st 
import openai
import os
import json
import base64

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
    edited_json = json.dumps(st.session_state.json_output, indent=2)
    b64 = base64.b64encode(edited_json.encode()).decode()
    href = f'<a href="data:file/json;base64,{b64}" download="{topic}.json">Download edited JSON file</a>'
    st.markdown(href, unsafe_allow_html=True)
except AttributeError:
    st.warning("Type a topic and generate some questions to refine them")

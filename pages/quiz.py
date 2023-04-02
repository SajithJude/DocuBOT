import streamlit as st 
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

DATA_DIR = "data"
# Get a list of available index files in the data directory
index_filenames = [f for f in os.listdir(DATA_DIR) if f.endswith(".json")]




book = st.selectbox("Select a Book ", index_filenames)
topic = st.text_input("Enter topic here")
# subtopic = st.text_input("Enter subtopic here")
num_quest = st.slider('Number of questions to generate', 0, 10, 1)
result = st.button("Submit")


if result:
    inut = "generate "+ str(num_quest)+ " questions with answers on the topic of "+str(topic)+", with the correct answers, show the output in json format."
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=inut,
        temperature=0.56,
        max_tokens=2100,
        top_p=1,
        frequency_penalty=0.35,
        presence_penalty=0
    )
    grading = response.choices[0].text.strip()
    st.write(grading)


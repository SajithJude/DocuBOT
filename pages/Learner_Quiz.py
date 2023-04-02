import streamlit as st
import json

st.set_page_config(page_title="Question-Answer Chatbot")

# Load the JSON file
def load_json(file):
    with open(file, "r") as f:
        data = json.load(f)
    return data

st.sidebar.title("User Responses")
responses = []

# Streamlit UI
st.title("Question-Answer Chatbot")

# File Upload
uploaded_file = st.file_uploader("Upload JSON file", type=["json"])

if uploaded_file:
    data = load_json(uploaded_file)
    st.success("File uploaded successfully!")
    st.write("Here are the available questions:")
    for i, item in enumerate(data):
        st.write(f"{i+1}. {item['question']}")

    # Chatbot
    st.write("Please answer the following questions:")
    for i, item in enumerate(data):
        st.write(f"Question {i+1}: {item['question']}")
        answer = st.text_input("Your Answer", key=i)
        responses.append(answer)

    # Sidebar
    st.sidebar.write(responses)

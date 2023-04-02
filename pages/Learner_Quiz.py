import streamlit as st
import json

st.set_page_config(page_title="Question-Answer Chatbot")

# Load the JSON file
def load_json(file):
    # Read the contents of the uploaded file as bytes
    file_contents = file.read()
    # Decode the bytes object to a string
    file_contents = file_contents.decode("utf-8")
    # Load the JSON string into a Python dictionary
    data = json.loads(file_contents)
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

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
    st.write("Please answer the following questions:")

    # Chatbot
    index = 0
    while index < len(data):
        question = data[index]
        st.write(f"Question {index+1}: {question['question']}")
        answer = st.text_input("Your Answer", key=index+1)
        if answer:
            responses.append({"question": question['question'], "answer": answer})
            index += 1
        else:
            st.warning("Please answer the current question before proceeding to the next one.")

    # Sidebar
    st.sidebar.write("Answered Questions:")
    for i, response in enumerate(responses):
        st.sidebar.write(f"{i+1}. {response['question']}")
        st.sidebar.write(f"   Answer: {response['answer']}")

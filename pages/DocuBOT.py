import os
import streamlit as st
from llama_index import GPTSimpleVectorIndex, SimpleDirectoryReader
import openai


openai.api_key = os.getenv("API_KEY")

DATA_DIR = "data"

# Define a function to load the index file and return the index object
@st.cache(allow_output_mutation=True)  # Use Streamlit's cache decorator to cache the function output
def load_index(selected_index):
    index_path = os.path.join(DATA_DIR, selected_index)
    index = GPTSimpleVectorIndex.load_from_disk(index_path)
    return index

# Get a list of available index files in the data directory
index_filenames = [f for f in os.listdir(DATA_DIR) if f.endswith(".json")]

# Add a selectbox to the Streamlit app for the user to choose an index file
selected_index = st.selectbox("Select an index to load", index_filenames)

# Add a button to the Streamlit app to load the selected index file
button = st.button("Load Index")

if button:
    index = load_index(selected_index)  # Call the `load_index` function to load the selected index
    st.success("Index loaded successfully.")

# Add a text input to the Streamlit app for the user to enter a question
ques = st.text_input("Enter a question")

# Add a button to the Streamlit app to query the index with the entered question
send = st.button("Ask")

if send:
    # Load the index if it hasn't been loaded yet
    if "index" not in st.session_state:
        st.session_state.index = load_index(selected_index)

    # Query the loaded index with the entered question
    index = st.session_state.index
    res = index.query(ques)

    # Display the results on the Streamlit app
    st.write(res)

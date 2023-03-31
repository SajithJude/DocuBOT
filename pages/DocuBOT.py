import streamlit as st
from llama_index import GPTSimpleVectorIndex, Document, SimpleDirectoryReader, QuestionAnswerPrompt
import os
import glob
import PyPDF2

import openai 
from streamlit_chat import message as st_message

favicon = "favicon.ac8d93a.69085235180674d80d902fdc4b848d0b (1).png"
st.set_page_config(page_title="DocuBOT", page_icon=favicon)


openai.api_key = os.getenv("API_KEY")

if "history" not in st.session_state:
    st.session_state.history = []

def new_chat():
    """
    Clears session state and starts a new chat.
    """
    st.session_state.history = []

col1, col2 = st.columns([2.2, 1])
col2.image("Flipick_Logo-1 (1).jpg", width=210)
st.write("")
st.write("")


DATA_DIR = "data"
# Get a list of available index files in the data directory
index_filenames = [f for f in os.listdir(DATA_DIR) if f.endswith(".json")]


if index_filenames:
    # If there are index files available, create a dropdown to select the index file to load
    index_file = st.selectbox("Select an index file to load:", index_filenames)
    index_path = os.path.join(DATA_DIR, index_file)
    index = GPTSimpleVectorIndex.load_from_disk(index_path)
else:
    # If there are no index files available, prompt the user to upload a PDF file
    st.warning("No index files found. Please upload a PDF file to create an index.")
    

def generate_answer():
    user_message = st.session_state.input_text
    query_str = str(user_message)
    context_str = "Generate answers for the questions that are relevant only to the documents context, throw a default answer saying I dont know for unrelevant questions."
    QA_PROMPT =  "When the users says quiz me, ask him a question from the context he mentioned, and corrext his answer on the next message"
    
    # QA_PROMPT = QuestionAnswerPrompt(QA_PROMPT_TMPL)
    message_bot = index.query(query_str, text_qa_template=QA_PROMPT, response_mode="compact", mode="embedding")
    st.session_state.history.append({"message": user_message, "is_user": True})
    st.session_state.history.append({"message": str(message_bot), "is_user": False})

if st.sidebar.button("New Chat"):
    new_chat()

input_text = st.text_input("Ask DocuBOT a question", key="input_text", on_change=generate_answer)

for chat in st.session_state.history:

    if chat["is_user"]:

        st.sidebar.caption("Question: " + chat["message"])
    else:
        with st.sidebar.expander("Bot Answer", expanded=False):
            st.write(chat["message"], language=None)

for chat in st.session_state.history:
    st_message(**chat)

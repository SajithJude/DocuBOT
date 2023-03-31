import streamlit as st
from llama_index import GPTSimpleVectorIndex, Document, SimpleDirectoryReader, QuestionAnswerPrompt
import os
import glob
import PyPDF2

import openai 
from streamlit_chat import message as st_message

favicon = "favicon.ac8d93a.69085235180674d80d902fdc4b848d0b (1).png"
st.set_page_config(page_title="Flipick Chat", page_icon=favicon)


openai.api_key = os.getenv("API_KEY")

if "history" not in st.session_state:
    st.session_state.history = []

col1, col2 = st.columns([2.2, 1])
col2.image("Flipick_Logo-1 (1).jpg", width=210)
st.write("")
st.write("")

# Get a list of all index files in the content directory
index_files = glob.glob("*.json")

if index_files:
    # If there are index files available, create a dropdown to select the index file to load
    index_file = st.selectbox("Select an index file to load:", index_files)
    index = GPTSimpleVectorIndex.load_from_disk(index_file)
else:
    # If there are no index files available, prompt the user to upload a PDF file
    st.warning("No index files found. Please upload a PDF file to create an index.")
    

def generate_answer():
    user_message = st.session_state.input_text
    
    if any(op in user_message for op in ['+', '-', '*', '/', '%']):
        st.session_state.history.append({"message": user_message, "is_user": True})
        st.session_state.history.append({"message": "I'm sorry, I'm not allowed to perform calculations.", "is_user": False})
    else:
        query_str = str(user_message)
        context_str = "Generate answers for the questions that are relevant only to the documents context, throw a default answer saying I dont know for unrelevant questions."
        QA_PROMPT_TMPL = (
            "We have provided context information below. \n"
            "---------------------\n"
            "{context_str}"
            "\n---------------------\n"
            "Given this information, please answer the question: {query_str}\n"
        )
        QA_PROMPT = QuestionAnswerPrompt(QA_PROMPT_TMPL)
        message_bot = index.query(query_str, text_qa_template=QA_PROMPT, response_mode="compact", mode="embedding")
        # source = message_bot.get_formatted_sources()
        # st.sidebar.write("Answer Source :",source)  # added line to display source on sidebar
        st.session_state.history.append({"message": user_message, "is_user": True})
        st.session_state.history.append({"message": str(message_bot), "is_user": False})

# if expander.expanded:
input_text = st.text_input("Ask flipick bot a question", key="input_text", on_change=generate_answer)
st.caption("Disclaimer : This ChatBOT is a pilot built solely for the purpose of a demo to Indian Institute of Banking and Finance (IIBF). The BOT has been trained based on the book Treasury Management published by IIBF. All content rights vest with IIBF")


# Display the conversation history
for chat in st.session_state.history:
    st_message(**chat)



















# import os
# import streamlit as st
# from llama_index import GPTSimpleVectorIndex, SimpleDirectoryReader
# import openai


# openai.api_key = os.getenv("API_KEY")

# DATA_DIR = "data"

# # Define a function to load the index file and return the index object
# @st.cache(allow_output_mutation=True)  # Use Streamlit's cache decorator to cache the function output
# def load_index(selected_index):
#     index_path = os.path.join(DATA_DIR, selected_index)
#     index = GPTSimpleVectorIndex.load_from_disk(index_path)
#     return index

# # Get a list of available index files in the data directory
# index_filenames = [f for f in os.listdir(DATA_DIR) if f.endswith(".json")]

# # Add a selectbox to the Streamlit app for the user to choose an index file
# selected_index = st.selectbox("Select an index to load", index_filenames)

# # Add a button to the Streamlit app to load the selected index file
# button = st.button("Load Index")

# if button:
#     index = load_index(selected_index)  # Call the `load_index` function to load the selected index
#     st.success("Index loaded successfully.")

# # Add a text input to the Streamlit app for the user to enter a question
# ques = st.text_input("Enter a question")

# # Add a button to the Streamlit app to query the index with the entered question
# # send = st.button("Ask")

# if ques:
#     # # Load the index if it hasn't been loaded yet
#     # if "index" not in st.session_state:
#     #     st.session_state.index = load_index(selected_index)

#     # Query the loaded index with the entered question
#     # index = st.session_state.index
#     res = index.query(ques)

#     # Display the results on the Streamlit app
#     st.write(res)

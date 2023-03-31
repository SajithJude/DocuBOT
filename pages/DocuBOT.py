import os
import streamlit as st
from llama_index import GPTSimpleVectorIndex, SimpleDirectoryReader
import openai


openai.api_key = os.getenv("API_KEY")




DATA_DIR = "data"

index_filenames = [f for f in os.listdir(DATA_DIR) if f.endswith(".bin")]
selected_index = st.selectbox("Select an index to load", index_filenames)
    

if selected_index:
    index_path = os.path.join(DATA_DIR, index_filename)
    index = GPTSimpleVectorIndex.load_from_disk(index_path)
    st.success("Index loaded succesfully.")

try:
    ques = st.text_input("enter question")
    res = index.query(ques)
    st.write(res)
except NameError:
    st.warninng("Select and index to get started")
import os
import streamlit as st
from llama_index import GPTSimpleVectorIndex, SimpleDirectoryReader
import openai


openai.api_key = os.getenv("API_KEY")




DATA_DIR = "data"

index_filenames = [f for f in os.listdir(DATA_DIR) if f.endswith(".json")]
selected_index = st.selectbox("Select an index to load", index_filenames)
button = st.button("Load Index")    

if button:
    index_path = os.path.join(DATA_DIR, selected_index)
    index = GPTSimpleVectorIndex.load_from_disk(index_path)
    st.success("Index loaded succesfully.")

ques = st.text_input("enter question")
if ques:
    res = index.query(ques)
    st.write(res)
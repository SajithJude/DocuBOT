import os
import streamlit as st
from llama_index import GPTSimpleVectorIndex, SimpleDirectoryReader
import openai


openai.api_key = os.getenv("API_KEY")


# Define the data directory path
DATA_DIR = "data"

# Create the data directory if it doesn't exist
if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)

# Define a function to save the uploaded file to the data directory
def save_uploaded_file(uploaded_file):
    with open(os.path.join(DATA_DIR, uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())

# Define the Streamlit app
def main():
    st.title("PDF Indexing App")
    
    # Create a file uploader widget
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    
    # Check if a file was uploaded
    if uploaded_file is not None:
        # Save the uploaded file to the data directory
        save_uploaded_file(uploaded_file)
        st.success("File saved successfully!")
    
    # Create a button to create the index
    if st.button("Create Index"):
        # Get the filename of the uploaded PDF
        pdf_filename = uploaded_file.name
        
        # Load the documents from the data directory
        documents = SimpleDirectoryReader(DATA_DIR).load_data()
        
        # Create the index from the documents
        index = GPTSimpleVectorIndex.from_documents(documents)
        
        # Save the index to the data directory with the same name as the PDF
        index.save_to_disk(os.path.join(DATA_DIR, os.path.splitext(pdf_filename)[0] + ".json"))
        st.success("Index created successfully!")
    
if __name__ == "__main__":
    main()

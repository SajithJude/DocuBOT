import os
import streamlit as st
from llama_index import GPTSimpleVectorIndex, SimpleDirectoryReader
import openai
from pathlib import Path
from llama_index import download_loader



openai.api_key = os.getenv("API_KEY")
PDFReader = download_loader("PDFReader")

loader = PDFReader()

# Define the data directory path
DATA_DIR = "data"

# Create the data directory if it doesn't exist
if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)


def display_pdf(DATA_DIR, pdf_file):
    with open(os.path.join(DATA_DIR, pdf_file), "rb") as f:
        pdf_reader = PyPDF2.PdfReader (f)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            with st.expander('Page'):
                st.write(page.extract_text())

def delete_pdf(DATA_DIR, pdf_file):
    os.remove(os.path.join(DATA_DIR, pdf_file))
    

# Define a function to save the uploaded file to the data directory
def save_uploaded_file(uploaded_file):
    with open(os.path.join(DATA_DIR, uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())

# Define the Streamlit app
def main():
    st.title("DocuBOT Admin")
    
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
    # Get a list of files in the directory
        files = os.listdir(DATA_DIR)

        colms = st.columns((4, 1, 1))

        fields = ["Name", 'View', 'Delete' ]
        for col, field_name in zip(colms, fields):
            # header
            col.subheader(field_name)

        i=1
        for  Name in files:
            i+=1
            col1, col2, col3 = st.columns((4 , 1, 1))
            # col1.write(x)  # index
            col1.caption(Name)  # email
            col2.button("View", key=Name, on_click=display_pdf, args=(DATA_DIR, Name))  # unique ID
            # col4.button(user_table['Delete'][x])   # email status
            delete_status = fields[0]  # flexible type of button
            button_type = "Delete" if delete_status else "Gone"
            button_phold = col3.empty()  # create a placeholder
            do_action = button_phold.button(button_type, key=i, on_click=delete_pdf, args=(DATA_DIR, Name))
            # if do_action:
            #         pass # do some action with a row's data
            #         button_phold.empty()  #  remove button
    
if __name__ == "__main__":
    main()
    

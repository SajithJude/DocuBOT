import os
import streamlit as st
import PyPDF2
from llama_index import GPTSimpleVectorIndex, SimpleDirectoryReader
import openai

# import streamlit as st
from streamlit.server.server import Server




# Define a function to get the current user's email address
def get_user_email():
    session_id = st._get_report_ctx().session_id
    session_info = Server.get_current()._get_session_info(session_id)
    user_email = session_info.session.request_headers["email"]
    return user_email

# Define a function to get the current user's permission level
def get_user_permission_level():
    # Here, we are just using a hardcoded permission level for demonstration purposes
    # You would replace this with your own logic for determining the user's permission level
    user_email = get_user_email()
    if user_email == "admin@example.com":
        return "admin"
    else:
        return "user"

# Define a function to check if the current user has permission to view a certain page
def user_has_permission_to_view_page(page_name):
    permission_levels = {
        "home": ["user", "admin"],
        "admin": ["admin"]
    }
    user_permission_level = get_user_permission_level()
    allowed_permission_levels = permission_levels.get(page_name, [])
    return user_permission_level in allowed_permission_levels


openai.api_key = os.getenv("API_KEY")
# PDFReader = download_loader("PDFReader")
# loader = PDFReader()

# Define the data directory path
DATA_DIR = "data"

# Create the data directory if it doesn't exist
if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)

# Define a function to display the contents of a PDF file
def display_pdf(DATA_DIR, pdf_file):
    with open(os.path.join(DATA_DIR, pdf_file), "rb") as f:
        pdf_reader = PyPDF2.PdfFileReader(f)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            with st.expander(f"Page {page_num+1}"):
                st.write(page.extractText())

# Define a function to delete a PDF file and its corresponding JSON index file
def delete_file(DATA_DIR, file_name):
    pdf_path = os.path.join(DATA_DIR, file_name)
    json_path = os.path.join(DATA_DIR, os.path.splitext(file_name)[0] + ".json")
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
        st.success(f"File {file_name} deleted successfully!")
    else:
        st.error(f"File {file_name} not found!")
    if os.path.exists(json_path):
        os.remove(json_path)

# Define a function to save the uploaded file to the data directory
def save_uploaded_file(uploaded_file):
    with open(os.path.join(DATA_DIR, uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())

# Define the Streamlit app
def main():
    if user_has_permission_to_view_page("admin"):

        st.title("DocuBOT Admin")
        
        # Create a file uploader widget
        uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
        
        # Check if a file was uploaded
        if uploaded_file is not None:
            # Save the uploaded file to the data directory
            save_uploaded_file(uploaded_file)
            st.success("File saved successfully!")
        
        # Create a button to create the index
        # if st.button("Create Index"):
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
        
        # Filter out the JSON index files
        files = [f for f in files if not f.endswith(".json")]

        colms = st.columns((4, 1, 1))

        fields = ["Name", 'View', 'Delete' ]
        for col, field_name in zip(colms, fields):
            # header
            col.subheader(field_name)

        i=1
        for Name in files:
            i+=1
            col1, col2, col3 = st.columns((4 , 1, 1))
            # col1.write(x)  # index
            col1.caption(Name)  # email
            if Name.endswith(".pdf"):
                col2.button("View", key=Name, on_click=display_pdf, args=(DATA_DIR, Name))  # unique ID
                delete_status = True
            else:
                col2.write("N/A")
                delete_status = False
            button_type = "Delete" if delete_status else "Gone"
            button_phold = col3.empty()  # create a placeholder
            do_action = button_phold.button(button_type, key=i, on_click=delete_file, args=(DATA_DIR, Name))
    else:

        st.subheader("Unauthorized")
        st.write("You are not authorized to view this page.")
                
    
if __name__ == "__main__":
    main()

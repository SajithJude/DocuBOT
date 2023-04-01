import streamlit as st
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationEntityMemory
from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from langchain.llms import OpenAI
from llama_index import GPTSimpleVectorIndex, Document, SimpleDirectoryReader, QuestionAnswerPrompt

import os 

# Set Streamlit page configuration
st.set_page_config(page_title='DocuBOT Quiz Mode', layout='wide')

# Initialize session states
if "generated" not in st.session_state:
    st.session_state["generated"] = []
if "past" not in st.session_state:
    st.session_state["past"] = []
if "input" not in st.session_state:
    st.session_state["input"] = ""
if "stored_session" not in st.session_state:
    st.session_state["stored_session"] = []
if "index" not in st.session_state:
    st.session_state["index"] = None

# Define function to get user input
def get_text():
    """
    Get the user input text.

    Returns:
        (str): The text entered by the user
    """
    input_text = st.text_input("You: ", st.session_state["input"], key="input",
                            placeholder="Ask Me to Quiz you from a chapter and correct your ...", 
                            on_change=submit_input,
                            on_submit=submit_input,
                            on_cancel=new_chat,
                            label_visibility='hidden')
    return input_text

# Define function to submit user input
def submit_input(input_text):
    """
    Submit user input and generate a response.
    """
    # Create an OpenAI instance
    llm = OpenAI(temperature=0,
                openai_api_key=API_O, 
                model_name="gpt-3.5-turbo", 
                verbose=False) 

    # Create a ConversationEntityMemory object if not already created
    if 'entity_memory' not in st.session_state:
        st.session_state.entity_memory = ConversationEntityMemory(llm=llm, k=3 )

    # Create the ConversationChain object with the specified configuration
    Conversation = ConversationChain(
        llm=llm, 
        prompt=ENTITY_MEMORY_CONVERSATION_TEMPLATE,
        memory=st.session_state.entity_memory
    )  

    # Generate the output using the ConversationChain object and the user input, and add the input/output to the session
    if st.session_state.index is not None:
        if input_text:
            response = st.session_state.index.query(input_text)
            if response is not None:
                output = response
                st.session_state.past.append(input_text)  
                st.session_state.generated.append(output)
    else:
        if input_text:
            output = Conversation.run(input=input_text)  
            st.session_state.past.append(input_text)  
            st.session_state.generated.append(output)

    st.session_state["input"] = ""

# Define function to start a new chat
def new_chat():
    """
    Clears session state and starts a new chat.
    """
    st.session_state["generated"] = []
    st.session_state["past"] = []
    st.session_state["input"] = ""
    st.session_state.entity_memory.store = {}
    st.session_state.entity_memory.buffer.clear()

# Set up the Streamlit app layout
st.title("DocuBot QuizMode")

# Ask the user to enter their OpenAI API key
API_O = os.getenv("API_KEY")

# Session state storage would be ideal

# Display the conversation history using an expander
with st.expander("Conversation", expanded=True):
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        st.info(st.session_state["past"][i],icon="🧐")
        st.success(st.session_state["generated"][i], icon="🤖")


for i, sublist in enumerate(st.session_state.stored_session):
    with st.sidebar.expander(label= f"Conversation-Session:{i}"):
        st.write(sublist)


if st.session_state.stored_session:
    if st.sidebar.checkbox("Clear-all"):
        del st.session_state.stored_session


if st.button("Start Over"):
    new_chat()
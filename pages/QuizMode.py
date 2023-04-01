import streamlit as st
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationEntityMemory
from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from langchain.llms import OpenAI
from llama_index import GPTSimpleVectorIndex

import os

st.set_page_config(page_title='DocuBOT Quiz Mode', layout='wide')

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

def get_text():
    input_text = st.text_input("You: ", st.session_state["input"], key="input",
                            placeholder="Ask Me to Quiz you from a chapter and correct your ...", 
                            label_visibility='hidden')
    # val = input_text
    # input_text = ""
    return input_text

def new_chat():
    save = []
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        save.append("User:" + st.session_state["past"][i])
        save.append("Bot:" + st.session_state["generated"][i])        
    st.session_state["stored_session"].append(save)
    st.session_state["generated"] = []
    st.session_state["past"] = []
    st.session_state["input"] = ""
    st.session_state.entity_memory.store = {}
    st.session_state.entity_memory.buffer.clear()

with st.sidebar.expander("Settings ", expanded=False):
    MODEL = st.selectbox(label='Model', options=['gpt-3.5-turbo','text-davinci-003','text-davinci-002','code-davinci-002'])
    K = st.number_input(' Number of Questions per quiz session',min_value=3,max_value=1000)

st.title("DocuBot QuizMode")

API_O = os.getenv("API_KEY")

llm = OpenAI(temperature=0,
            openai_api_key=API_O, 
            model_name=MODEL, 
            verbose=False) 

if 'entity_memory' not in st.session_state:
    st.session_state.entity_memory = ConversationEntityMemory(llm=llm, k=K )

Conversation = ConversationChain(
    llm=llm, 
    prompt=ENTITY_MEMORY_CONVERSATION_TEMPLATE,
    memory=st.session_state.entity_memory
)  

if st.session_state.index is not None:
    user_input = get_text()
    if user_input:
        response = st.session_state.index.query(user_input)
        if response is not None:
            output = response
            st.session_state.past.append(user_input)  
            st.session_state.generated.append(output)
            st.session_state["input"] = "" 
else:
    user_input = get_text()
    if user_input:
        output = Conversation.run(input=user_input)  
        st.session_state.past.append(user_input)  
        st.session_state.generated.append(output)  
        st.session_state["input"] = "" 

download_str = []

with st.expander("Conversation", expanded=True):
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        st.info(st.session_state["past"][i],icon="🧐")
        st.success(st.session_state["generated"][i], icon="🤖")
        download_str.append(st.session_state["past"][i])
        download_str.append(st.session_state["generated"][i])
    
    download_str = '\n'.join(download_str)
    if download_str:
        st.download_button('Download',download_str)

for i, sublist in enumerate(st.session_state.stored_session):
    with st.sidebar.expander(label= f"Conversation-Session:{i}"):
        st.write(sublist)

if st.session_state.stored_session:   
    if st.sidebar.checkbox("Clear-all"):
        del st.session_state.stored_session




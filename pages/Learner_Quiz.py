import streamlit as st
from streamlit_chat import message
import json

st.set_page_config(
    page_title="Streamlit Chat - Demo",
    page_icon=":robot:"
)

st.header("Streamlit Chat - Demo")

with open("questions.json") as f:
    questions = json.load(f)

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []
    
if 'current_question' not in st.session_state:
    st.session_state['current_question'] = 0

def get_text():
    input_text = st.text_input("You: ","", key="input")
    return input_text 

if st.session_state['current_question'] < len(questions):
    current_question = questions[st.session_state['current_question']]
    message(current_question['question'], is_user=False, key=str(st.session_state['current_question']))
    user_input = get_text()

    if user_input:
        st.sidebar.write(current_question['question'])
        st.sidebar.write("You: ", user_input)
        
        message(current_question['answer'], is_user=False, key=str(st.session_state['current_question']) + '_answer')
        st.session_state['current_question'] += 1

if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
        st.sidebar.write("Bot: ", st.session_state["generated"][i])

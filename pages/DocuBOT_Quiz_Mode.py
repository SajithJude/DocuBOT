import streamlit as streamlit
from streamlit_chat import message
import json

streamlit.set_page_config(
    page_title="Streamlit Chat - Demo",
    page_icon=":robot:"
)

streamlit.header("DocuBOT QuizMode")

uploaded_file = streamlit.file_uploader("Choose a file")

if uploaded_file is not None:
    questions = [q['question'] for q in json.load(uploaded_file)]
    
    if 'generated' not in streamlit.session_state:
        streamlit.session_state['generated'] = []

    if 'past' not in streamlit.session_state:
        streamlit.session_state['past'] = []
        
    if 'current_question' not in streamlit.session_state:
        streamlit.session_state['current_question'] = 0

    def get_text():
        input_text = streamlit.text_input("You: ","", key="input")
        return input_text 

    if streamlit.session_state['current_question'] < len(questions):
        current_question = questions[streamlit.session_state['current_question']]
        message(current_question, is_user=False, key=str(streamlit.session_state['current_question']))
        user_input = get_text()

        if user_input:
            streamlit.session_state['past'].append(user_input)
            streamlit.session_state['current_question'] += 1

        streamlit.sidebar.header("Conversation History")
        for i, question in enumerate(questions):
            if i < streamlit.session_state['current_question']:
                streamlit.sidebar.write(question)
                streamlit.sidebar.write("You: " + streamlit.session_state['past'][i])

    else:
        responses = []
        for i, question in enumerate(questions):
            response = {
                "question": question,
                "response": streamlit.session_state['past'][i]
            }
            responses.append(response)
        
        with open("responses.json", "w") as outfile:
            json.dump(responses, outfile)

        message("Thank you for answering all the questions. Your responses have been saved.", is_user=False)
        streamlit.sidebar.write("Thank you for answering all the questions. Your responses have been saved.")

        streamlit.sidebar.download_button(
            label="Download Responses",
            data=json.dumps(responses),
            file_name="responses.json",
            mime="application/json"
        )
        
    if streamlit.session_state['generated']:
        for i in range(len(streamlit.session_state['generated'])-1, -1, -1):
            message(streamlit.session_state["generated"][i], key=str(i))
            message(streamlit.session_state['past'][i], is_user=True, key=str(i) + '_user')
            streamlit.sidebar.write("Bot: ", streamlit.session_state["generated"][i])

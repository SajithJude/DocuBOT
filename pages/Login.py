import streamlit as st

# Create a card container with shadow effect
container = st.container()
container.markdown(
    f'<div style="border-radius: 10px; box-shadow: 0px 0px 5px 2px rgba(0, 0, 0, 0.1); padding: 20px;">'
    f'<h2 style="text-align: center;">Login Form</h2>'
    f'<form>'
    f'<label for="email">Email:</label><br>'
    f'<input type="email" id="email" name="email"><br>'
    f'<label for="password">Password:</label><br>'
    f'<input type="password" id="password" name="password"><br><br>'
    f'<input type="submit" value="Submit">'
    f'</form>'
    f'</div>', unsafe_allow_html=True)

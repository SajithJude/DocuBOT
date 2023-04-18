import streamlit as st

# Create a card container with shadow effect
container = st.container()
container.markdown(
    f'<div style="border-radius: 10px; box-shadow: 0px 0px 5px 2px rgba(0, 0, 0, 0.1); padding: 20px;">'
    f'<h2 style="text-align: center;">Login Form</h2>'
    f'</div>', unsafe_allow_html=True)

# Add input fields to the container
with st.container():
    email = container.text_input("Email")
    password = container.text_input("Password", type="password")

# Add submit button to the container
if container.button("Submit"):
    st.write(f"Email: {email}")
    st.write(f"Password: {password}")

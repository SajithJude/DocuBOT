import streamlit as st

container = st.container()

with container:
    tab1, tab2 = st.tabs(["login", "register"])

    with tab1:
        st.subheader("Login")
        user_type = st.radio("Select user type", ("student", "instructor"))
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            # Login button logic goes here
            pass

    with tab2:
        st.subheader("Register")

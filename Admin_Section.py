import firebase_admin
from firebase_admin import credentials, firestore

import streamlit as st
from pyrebase import pyrebase




cred = credentials.Certificate("docubot-2ac1d-firebase-adminsdk-9ztu6-80050a35cd.json")
firebase_admin.initialize_app(cred)

# Initialize Pyrebase with the Firebase project credentials
config = {
    "apiKey": "AIzaSyCnP2MswW3g6zpdNP0hx3aviXCej2ZmC0c",
    "authDomain": "docubot-2ac1d.firebaseapp.com",
    "projectId": "docubot-2ac1d",
    "storageBucket": "docubot-2ac1d.appspot.com",
    "messagingSenderId": "1053457031443",
    "appId": "1:1053457031443:web:82e2dbbf519bd97435bae6",
    "measurementId": "G-DM2R9ECXRV"
}
firebase = pyrebase.initialize_app(config)

# Define the registration form
def register():
    st.subheader("Create a new account")
    name = st.text_input("Name")
    institute = st.text_input("Institute")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    role = st.selectbox("User Role", ["learner", "instructor"])
    if st.button("Register"):
        try:
            auth = firebase.auth()
            user = auth.create_user_with_email_and_password(email, password)
            db = firebase.firestore()
            db.collection("users").document(user["localId"]).set({
                "name": name,
                "institute": institute,
                "email": email,
                "role": role
            })
            st.success("Account created!")
        except Exception as e:
            st.error(e)

# Define the Streamlit app
def app():
    st.title("User Management App")
    menu = ["Home", "Login", "Register"]
    choice = st.sidebar.selectbox("Select an option", menu)
    if choice == "Home":
        st.subheader("Welcome to the User Management App")
    elif choice == "Login":
        # Define the login form
        st.subheader("Login to your account")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            try:
                auth = firebase.auth()
                auth.sign_in_with_email_and_password(email, password)
                st.success("Logged in!")
            except Exception as e:
                st.error(e)
    elif choice == "Register":
        # Show the registration form
        register()

if __name__ == "__main__":
    app()

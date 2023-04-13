import streamlit as st
import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore, auth

cred = credentials.Certificate("docubot-2ac1d-firebase-adminsdk-9ztu6-80050a35cd.json")

def assign_assessment(user_id: str, assessment: dict):
    db = firestore.client()
    user_ref: DocumentReference = db.collection("users").document(user_id)
    user_ref.set({"assessment": assessment}, merge=True)
    return True


# Initialize Pyrebase with the Firebase project credentials
config = {
    "apiKey": "AIzaSyCnP2MswW3g6zpdNP0hx3aviXCej2ZmC0c",
    "authDomain": "docubot-2ac1d.firebaseapp.com",
    "projectId": "docubot-2ac1d",
    'databaseURL': "https://docubot-2ac1d-default-rtdb.asia-southeast1.firebasedatabase.app/",
    "storageBucket": "docubot-2ac1d.appspot.com",
    "messagingSenderId": "1053457031443",
    "appId": "1:1053457031443:web:82e2dbbf519bd97435bae6",
    "measurementId": "G-DM2R9ECXRV"
}
firebase = pyrebase.initialize_app(config)

firebase = pyrebase.initialize_app(config)

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
            db = firestore.client()

            db.collection("users").document(user["localId"]).set({
                "name": name,
                "institute": institute,
                "email": email,
                "role": role
            })
            st.success("Account created!")
        except Exception as e:
            st.error(e)

st.title("Docubot Flipick")
menu = ["Home", "Login", "Register"]
choice = st.selectbox("Select an option", menu)
if choice == "Home":
    st.subheader("Welcome to the User Management App")
    
elif choice == "Login":
    st.subheader("Login to your account")
    email = st.text_input("Email", value=st.session_state.get("email", ""))
    password = st.text_input("Password", type="password", value=st.session_state.get("password", ""))
    if st.button("Login"):
        try:
            Auth = firebase.auth()
            db = firestore.client()
            Auth.sign_in_with_email_and_password(email, password)
            st.success("Logged in!")
            user = auth.get_user_by_email(email)
            if user is not None:
                role = db.collection("users").document(user.uid).get().to_dict().get("role")
                if role == "instructor":
                    learners = db.collection("users").where("role", "==", "learner").get()
                    st.subheader("List of Learners:")
                    for learner in learners:
                        st.write(f"- {learner.to_dict()['name']}")

                    # Add Assign Assessment button and input field
                    assessment_json = st.session_state.json_output
                    st.session_state.selected_learner = st.selectbox("Select Learner to Assign Assessment", [learner.to_dict()["name"] for learner in learners], key="learner_selection")

                    # st.session_state.selected_learner = selected_learner
                    assign_button = st.button("Assign Assessment")

                    if assign_button and st.session_state.selected_learner:

                        # Find the selected learner's ID
                        selected_learner_id = None
                        for learner in learners:
                            if learner.to_dict()["name"] == st.session_state.selected_learner:
                                selected_learner_id = learner.id
                                st.write(selected_learner_id)
                                break

                        # Assign the assessment to the selected learner
                        try:
                            assessment_data = json.loads(assessment_json)
                            if assign_assessment(selected_learner_id, assessment_data):
                                st.success(f"Assessment assigned to {st.session_state.selected_learner}")
                            else:
                                st.error("Failed to assign assessment")
                        except Exception as e:

                            st.error(f"Invalid JSON format: {e}")
        except Exception as e:
            st.error(e)                        
elif choice == "Register":

# Show the registration form
    register()
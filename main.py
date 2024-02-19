import pickle
import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import numpy as np
import sqlite3

# Load the heart disease prediction model
heart_disease_model = pickle.load(
    open('C:/Users/Asus/Desktop/python_venv/Heart_Disease_Prediction/saved_models/heart_disease_model.sav', 'rb'))

# Create a SQLite database and a table for user information
conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT
    )
''')
conn.commit()

def is_user_exists(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    return cursor.fetchone() is not None

def is_username_exists(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    return cursor.fetchone() is not None

def create_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    conn.commit()

def login(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    if user:
        return True
    return False

# Sidebar for navigation
with st.sidebar:
    selected = option_menu('Heart Disease Prediction System',
                           ['Register',
                           'Login',
                            'Heart Disease Prediction',
                            'Heart Disease Prevention Guide',
                            'Logout'],
                           icons=['file-earmark-person', 'person', 'activity', 'box-arrow-right'],
                           default_index=0)

if selected == "Login":
    st.header("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if login(username, password):
            st.success("Logged in as " + username)
            st.session_state.logged_in = True
        else:
            st.error("Invalid username or password")
            st.session_state.logged_in = False

if selected == "Register":
    st.header("Register")
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    if new_password == confirm_password:
        if st.button("Register"):
            if new_username and new_password:
                if is_username_exists(new_username):
                    st.error('Username already exists. Please choose a different one.')
                else:
                    create_user(new_username, new_password)
                    st.success("Registration successful. You can now log in.")
    else:
        st.error("Passwords do not match")

if selected == "Heart Disease Prediction":
    st.title("Heart Disease Prediction using ML")

    if st.session_state.get("logged_in", False):

        age = st.number_input('Enter your Age - between 27 to 77', min_value=27, max_value=77, format="%d", key="age", step=1, value=27, help="Enter your age")
        sex = st.number_input('Sex (0 for female & 1 for male)', value=0, min_value=0, max_value=1, step=1, format="%d")
        cp = st.number_input('Chest Pain types (0 for asymptomatic, 1 for atypical angina, 2 for non-anginal pain, and 3 for typical angina)', value=0, min_value=0, max_value=3, step=1, format="%d")
        trestbps = st.number_input('Resting Blood Pressure in mm Hg (94-200 mm Hg)',value=94, min_value=94, max_value=200, step=1, format="%d")
        chol = st.number_input('Serum Cholesterol in mg/dL (126-564 mg/dL)',value=126, min_value=126, max_value=564, step=1, format="%d")
        fbs = st.number_input('Fasting Blood Sugar (0 for FBS <= 120 mg/dL and 1 for FBS > 120 mg/dL)', value=0, min_value=0, max_value=1, step=1, format="%d")
        restecg = st.number_input('Resting Electrocardiographic results (0 for normal, 1 for having ST-T wave abnormality, and 2 for showing probable or definite left ventricular hypertrophy)', min_value=0, max_value=2, step=1, format="%d")
        thalach = st.number_input('Maximum Heart Rate achieved (71-202 bpm)', value=71, min_value=71, max_value=202, step=1, format="%d")
        exang = st.number_input('Exercise Induced Angina (0 for no Exercise-Induced Angina and 1 for Exercise-Induced Angina)', value=0, min_value=0, max_value=1, step=1, format="%d")
        oldpeak = st.number_input('ST depression induced by exercise (0.0-6.2)', value=0.0, min_value=0.0, max_value=6.2, step=0.1, format="%.1f")
        slope = st.number_input('Slope of the peak exercise ST segment (0 for downsloping, 1 for flat, and 2 for upsloping)', value=0, min_value=0, max_value=2, step=1, format="%d")
        ca = st.number_input('Major vessels colored by fluoroscopy (0-3)', value=0, min_value=0, max_value=3, step=1, format="%d")
        thal = st.number_input('Thal (1 = normal; 2 = fixed defect; 3 = reversable defect)', value=1, min_value=1, max_value=3, step=1, format="%d")

        # Add an image upload widget
        uploaded_image = st.file_uploader("Upload an Heart Scan Image", type=["jpg", "png", "jpeg"])

        # code for Prediction
        heart_diagnosis = ''

        # creating a button for Prediction
        if st.button('Heart Disease Test Result'):

            if uploaded_image is not None:
                # Process the uploaded image
                image = Image.open(uploaded_image)
                # Perform image processing or feature extraction as needed
                image_data = np.array(image)  # Convert the image to a numpy array

            heart_prediction = heart_disease_model.predict(
                [[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]])

            if (heart_prediction[0] == 1):
                heart_diagnosis = 'The person is having heart disease'
            else:
                heart_diagnosis = 'The person does not have any heart disease'

        st.success(heart_diagnosis)

    else:
        st.warning("Please log in to access this page.")

if selected == "Heart Disease Prevention Guide":
    st.title("Heart Disease Prevention Guide")

    if st.session_state.get("logged_in", False):

        st.write("Here are some useful YouTube videos for Heart Disease Prevention:")
        video_urls = [
            "https://www.youtube.com/watch?v=3jPcmD2Jq24",
            "https://www.youtube.com/watch?v=220T1PGO77o",
            "https://www.youtube.com/watch?v=02SL-xxeiNw",
            "https://www.youtube.com/watch?v=_ePLBIDlChA",
            # Add more YouTube video URLs as needed
        ]

        for video_url in video_urls:
            st.video(video_url)

    else:
        st.warning("Please log in to access this page.")
        print("I'm warning")


if selected == "Logout":
    st.session_state.logged_in = False
    st.success("You have been logged out.")

# Close the database connection when the Streamlit app is done
conn.close()



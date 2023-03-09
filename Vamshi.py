import streamlit as st
import pickle
from streamlit_option_menu import option_menu
import sqlite3

# Connect to the database
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create the users table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)''')
conn.commit()


# sidebar for navigation
with st.sidebar:
    selected = option_menu('Mental Health Prediction System',
                           [
                            'Home Page',
                            'Mental Health Prediction',
                            'Login',
                            'Register'
                           ],
                           icons=['activity', 'heart', 'person'],
                           default_index=0)
# Heart Disease Prediction Page
# Login page
if selected == 'Login':
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    if st.button("Submit"):
        cursor.execute(f"SELECT * FROM users WHERE username='{username}' AND password='{password}'")
        user = cursor.fetchone()
        if user:
            st.success("Logged in!")
            st.sidebar.checkbox("Login", value=True, key="login")
        else:
            st.error("Incorrect username or password.")

# Register page
elif selected == 'Register':
    st.title("Register")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    confirm_password = st.text_input("Confirm Password", type='password')
    if st.button("Submit"):
        if password == confirm_password:
            cursor.execute(f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')")
            conn.commit()
            st.success("Registered!")
        else:
            st.error("Passwords do not match.")
if selected == 'Mental Health Prediction':
    if not st.sidebar.checkbox("Login", key="login"):
        st.error("Please login to access this page.")
    
    else:
        st.text("Please answer the below questions to predict whether or not you are suffering from \nany mental health issue.\n")
        age = st.slider("Age", min_value=7, max_value=90, value=50, step=1)
        if age < 10:
            age = age/10
        elif age < 100:
            age = age/100

    # Gender input
        st.text("Gender")
        gender_options = ["Male", "Female", "Trans"]
        gender = st.radio("Gender", gender_options)
        if gender == "Male":
            gender = 1
        elif gender == "Female":
            gender = 0
        else:
            gender = 2

# Hereditary input
        st.text("Is the problem you are facing hereditary?")
        hereditary_options = ["Yes", "No"]
        hereditary = st.radio("Hereditary", hereditary_options)
        if hereditary == "Yes":
            hereditary = 0
        else:
            hereditary = 1

# Benefits input
        st.text("Are you availing any benefits from your organization in the view of \nyour health issue?")
        benefits_options = ["Don't know", "No","Yes"]
        benefits = st.radio("Benefits", benefits_options)
        if benefits == "Don't know":
            benefits = 0
        elif benefits == "No":
            benefits = 1
        elif benefits == "Yes":
            benefits = 2

# Taking care input
        st.text("Are you taking any care of the issue you are facing that is actually helping?")
        care_options = ["No", "Not sure", "Yes"]
        care = st.radio("Taking care", care_options)
        if care == "No":
            care = 0
        elif care == "Not sure":
            care = 1
        else:
            care = 2

# Anonymous input
        st.text("Are you willing to stay anonymous about your health issue?")
        anonymous_options = ["Don't know", "No", "Yes"]
        anonymous = st.radio("Anonymous", anonymous_options)
        if anonymous == "Don't know":
            anonymous = 0
        elif anonymous == "No":
            anonymous = 1
        else:
            anonymous = 2

# Health leaves input
        st.text("Do you get enough health leaves to take care of yourself?")
        leaves_options = ["Don't know", "Somewhat difficult", "Somewhat easy", "Very difficult", "Very easy"]
        leaves = st.radio("Health leaves", leaves_options)
        if leaves == "Don't know":
            leaves = 0
        elif leaves == "Somewhat difficult":
            leaves = 1
        elif leaves == "Somewhat easy":
            leaves = 2
        elif leaves == "Very difficult":
            leaves = 3
        else:
            leaves = 4

# Interfering with work input
        st.text("Is your condition interfering with your work?")
        work_options = ["Don't know", "Never", "Often", "Rarely", "Sometimes"]
        work = st.radio("Interfering with work", work_options)
        if work == "Don't know":
            work = 0
        elif work == "Never":
            work = 1
        elif work == "Often":
            work = 2
        elif work == "Rarely":
            work = 3
        else:
            work = 4
# Loading the saved model
        model = pickle.load(open("/home/mr1ncr1d1ble/Downloads/model.pkl", "rb"))

# Predicting the output
        input_data = [age, gender, hereditary, benefits, care, anonymous, leaves, work]

        if st.button("Predict"):
            prediction = model.predict([input_data])
            if prediction == 0:
                st.text("You are not suffering from any mental health issue.")
            else:
                st.text("You are suffering from some mental health issue. \nPlease take care of yourself by consulting a doctor.")
    

elif selected == 'Home Page':
    st.markdown(""" <style> .font {
            font-size:50px ; font-family: 'Cooper Black'; color: #FF0000;} 
            </style> """, unsafe_allow_html=True)
    st.markdown('<p class="font">Mental health Prediction Application</p>', unsafe_allow_html=True)


    img_url="https://xyz-field.com/wp-content/uploads/2022/11/Mind-Matters-blog-banner.jpg"
    st.image(img_url, caption="mental health",use_column_width=True)
    st.text("The aim of the project is to help a person going through any mental issue understand \nthe seriousness of their condition and help them in deciding whether they need help \nfrom a professional or not. This application is suitable for you if your age is \nanywhere above 7. \nYou can answer 8 simple questions after which our model predicts whether you need \nhelp or you can cope up on your own.\n")





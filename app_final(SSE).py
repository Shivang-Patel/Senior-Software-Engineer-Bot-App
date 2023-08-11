import streamlit as st
import requests
# import pymongo
import random
import openai

# API URLs
QUESTION_API_URL = "https://axisapi.onrender.com/Question"
ASSESS_API_URL = "https://axisapi.onrender.com/Assess"
SUBMIT_API_URL= "https://axisapi.onrender.com/submit"

# Fixed job description
FIXED_JOB_DESCRIPTION = "Senior Software Engineer"

# Function to get interview questions
def get_interview_questions():
    params = {
        'description': FIXED_JOB_DESCRIPTION
    }

    response = requests.get(QUESTION_API_URL, params=params)
    data = response.json()
    return data['questions']

# Function to calculate and display the score
def calculate_and_display_score(questions, answers, email):
    params = {
        'questions': questions,
        'answers': answers,
        'email': email
    }

    response = requests.get(ASSESS_API_URL, params=params)
    if response.status_code == 200:
        score_data = response.json()
        return score_data['score']
    else:
        return None
    
def final_submission(email, score, job_id):
    params = {
        'email': email,
        'score': score,
        'job_id': job_id
    }

    response= requests.post(SUBMIT_API_URL, params=params)
    if response.status_code == 200:
        print('POST request successful')
        print('Response:', response.text)
    else:
        print('POST request failed')
        print('Status code:', response.status_code)
        print('Response:', response.text)

    

# Function to save data to MongoDB
# def save_to_mongodb(email, score):
#     client = pymongo.MongoClient("mongodb+srv://mahirakajaria:NL1htAGffe0TLscA@cluster0.estoffi.mongodb.net/")
#     db = client["test"]
#     # collection = db['testScore']
#     user_collection = db['users']
#     cvs_collection = db['cvs']

#     user = user_collection.find_one({'email': email})

#     if user:
#         user_id = user['_id']
#     else:
#         print("Candidate email not found.")
#         exit()
    
#     job_id = "6789"  # Replace with the actual job ID

#     update_result = cvs_collection.update_one(
#         {'jobId': job_id, 'owner': user_id},
#         {'$set': {'testScore': score}}
#     )

#     entry = {
#         'jobid': job_id,
#         'email': email,
#         'score': score
#     }
#     # collection.insert_one(entry)
#     client.close()


# ...

def initialize_session_state():
    if "questions" not in st.session_state:
        st.session_state.questions = get_interview_questions()

    if "question_index" not in st.session_state:
        st.session_state.question_index = 0
        st.session_state.answers = []

def main():
    st.title("xsBot.ai")
    
    st.write(f"Role: {FIXED_JOB_DESCRIPTION}")
    
    initialize_session_state()

    email = st.text_input("Enter your email:")
    
    question_index = st.session_state.question_index
    questions = st.session_state.questions
    
    if question_index < len(questions):
        current_question = questions[question_index]
        answer = st.text_area(f"Q{question_index+1}: {current_question}")
        st.session_state.answers.append(answer)
        
        if st.button("Next"):
            st.session_state.question_index += 1
    else:
        st.write("All questions answered. Click 'Submit' to see your score.")
    
    if st.button("Submit"):
        answers = st.session_state.answers
        score = calculate_and_display_score(questions, answers, email)
        
        if score is not None:
            st.success(f"Your Score: {score}")
            # save_to_mongodb(email, score)
            final_submission(email, score, "6789")

if __name__ == "__main__":
    main()

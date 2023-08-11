import streamlit as st
import requests
# import pymongo
import random
# import openai

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


def initialize_session_state():
    if "questions" not in st.session_state:
        st.session_state.questions = get_interview_questions()

    if "question_index" not in st.session_state:
        st.session_state.question_index = 0

    if "answers" not in st.session_state:
        st.session_state.answers = []


def main():
    st.title("xsBot.ai")
    
    st.write(f"Role: {FIXED_JOB_DESCRIPTION}")
    
    initialize_session_state()

    email = st.text_input("Enter your email:")
    
    question_index = st.session_state.question_index
    questions = st.session_state.questions

    final_score=0
    
    if question_index < len(questions):
        current_question = questions[question_index]
        
        # Use a unique key for each text_area to avoid rendering issues
        answer = st.text_input(f"Q{question_index+1}: {current_question}", key=f"answer_{question_index}")
        
        if st.button("Next"):
            st.session_state.answers.append(answer)  # Append answer to the list
            
            # Calculate the score for the current question
            score = calculate_and_display_score([current_question], [answer], email)
            
            # Display the calculated score for the current question
            if score is not None:
                st.write(f"Score for Q{question_index+1}: {score}")
                final_score = final_score + score
            
            st.session_state.question_index += 1
    else:
        st.write("All questions answered. Click 'Generate Score' to see your score.")
    
    if st.button("Generate Score"):
        answers = st.session_state.answers
        # score = calculate_and_display_score(questions, answers, email)
        st.success(f"Your Score: {final_score}")
        st.write("You can now close the tab")
        
        # # if score is not None:
        #     st.success(f"Your Score: {score}")
        #     final_submission(email, score, "6789")


if __name__ == "__main__":
    main()

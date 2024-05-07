# this file is for listening for user requests

# steps for the processRequest listener
# 1. listen for user requests and receive them, user requests will consist of a number, representing the number of days they want the summary for
# 2. this request is sent to the Prompter.prompt() function
# 3. This response is parsed by the response parser and sent back to the user

# Also support login, logout, and user onboarding functions on various endpoints
from datetime import datetime, timezone, timedelta
from time import sleep

import sys
sys.path.append("../src")

from Prompter.Prompter import Prompter
# from src.ResponseParser.ResponseParser import ResponseParser
from UserManagement.UserManager import UserManager


def processRequest():
    # data = request.get_json()
    data = {'days': 1}
    days = data['days']
    startDate = datetime.now(timezone.utc) - timedelta(days=days)
    prompter = Prompter("Summarize the following message data from various sources")
    response = prompter.prompt(startDate)
    # response_parser = ResponseParser()
    # response = response_parser.parse(response)
    # print(response)
    return response



def login(data):
    username = data['username']
    password = data['password']
    user_manager = UserManager()
    response = user_manager.login(username, password)
    # print(response)
    print('Logged in')

# def logout():
#     user_manager = UserManager()
#     response = user_manager.logout()
#     return jsonify(response)

def onboarding(data):

    # username, email, password, gemini_api_key, openai_api_key, slack_email, slack_id
    
    username = data['username']
    email = data['email']
    password = data['password']
    gemini_api_key = data['gemini_api_key']
    openai_api_key = data['openai_api_key']
    slack_email = data['slack_email']
    slack_id = data['slack_id']

    user_manager = UserManager()
    user_manager.store_user_data(
        username=username,
        email=email,
        password=password,
        gemini_api_key=gemini_api_key,
        openai_api_key=openai_api_key,
        slack_email=slack_email,
        slack_id=slack_id
    )

    print('User onboarding over')

# onboarding({'username': 'raghav', 'email': 'raghav.donakanti@students.iiit.ac.in','password':'hello123','gemini_api_key':'AIzaSyAnyGrLk1KZMbQ630X2b9WlgZxIHuSTd4Q','openai_api_key':'sk-proj-sNnochKA6hIWBNrw6JUAT3BlbkFJMPf1wRZgrKk5Ah1vfQhX','slack_email':'raghav.donakanti@students.iiit.ac.in','slack_id': 'hfjjgfjgfg'})

onboarding({'username': "raghav", 'email': "raghav.donakanti@students.iiit.ac.in",'password': "hello123",'gemini_api_key': "AIzaSyAnyGrLk1KZMbQ630X2b9WlgZxIHuSTd4Q",'openai_api_key': "sk-proj-sNnochKA6hIWBNrw6JUAT3BlbkFJMPf1wRZgrKk5Ah1vfQhX",'slack_email': "raghav.donakanti@students.iiit.ac.in",'slack_id': "hfjjgfjgfg"})

login({'username': "raghav", 'password': "hello123"})

sleep(10)
print('start')

processRequest()


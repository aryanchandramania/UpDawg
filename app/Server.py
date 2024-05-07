# this file is for listening for user requests

# steps for the processRequest listener
# 1. listen for user requests and receive them, user requests will consist of a number, representing the number of days they want the summary for
# 2. this request is sent to the Prompter.prompt() function
# 3. This response is parsed by the response parser and sent back to the user

# Also support login, logout, and user onboarding functions on various endpoints

from flask import Flask, request, jsonify
import sys
sys.path.append("../src")

from Prompter.Prompter import Prompter
from ResponseParsing.ResponseParsing import ResponseParser
from UserManagement.UserManager import UserManager

import datetime
from datetime import timezone

app = Flask(__name__)

@app.route('/processRequest', methods=['POST'])
def processRequest():
    data = request.get_json()
    days = int(data['days'])
    startDate = datetime.datetime.now(timezone.utc) - datetime.timedelta(days=days)
    prompter = Prompter("Summarize the following message data from various sources")
    response = prompter.prompt(startDate)
    response_parser = ResponseParser()
    response = response_parser.get_clean_response(response)
    response_parser.save_response(response)
    res = {'message': response}
    return jsonify(res)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    user_manager = UserManager()
    response = user_manager.login(username, password)
    res = {'message': ('OK' if response else 'Failed')}
    return jsonify(res)

@app.route('/logout', methods=['POST'])
def logout():
    user_manager = UserManager()
    response = user_manager.logout()
    res = {'message': ('OK' if response else 'Failed')}
    return jsonify(res)

@app.route('/onboarding', methods=['POST'])
def onboarding():

    response_parser = ResponseParser()
    response_parser.create_response_file()

    # username, email, password, gemini_api_key, openai_api_key, slack_email, slack_id
    data = request.get_json()
    
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


@app.route('/getSumm', methods=['GET'])
def getSumm():
    response_parser = ResponseParser()
    summaries = response_parser.get_user_summaries()
    res = {'message': summaries}
    return jsonify(res)








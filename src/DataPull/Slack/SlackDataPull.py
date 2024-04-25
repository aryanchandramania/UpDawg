from slack_sdk import WebClient 
from slack_sdk.errors import SlackApiError 
import json
import datetime
import configparser
import asyncio

import sys
sys.path.append('../..')
from DataPull.DataPull import DataPull
from Message.Message import Message

"""
history.json format:
{
    "channel_name": [
        {
            "user": "user_name",
            "time": "time",
            "text": "message"
        },
        ...
    ],
    ...
}
"""

class SlackDataPull(DataPull):    
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.cfg')
        self.slack_token = config['SLACK']['SLACK_TOKEN']
        self.client = WebClient(token=self.slack_token)	
        self.id_to_channel = {}
        self.id_to_user = {}
        self.history_json = {}

    def convert_ts_to_date(self, ts):
        return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    
    def convert_date_to_ts(self, date):
        return datetime.datetime.timestamp(date)

    def too_old(self, ts, start_time: datetime):    
        return datetime.datetime.fromtimestamp(ts) < start_time
    
    def nzprint(self, text, value, ztext="results"):
        if value != 0:
            print(text)
        else:
            print("No ", ztext, " found.")

    def get_channel(self, id):
        if id in self.id_to_channel:
            return self.id_to_channel[id]
        return "Unknown channel"

    def get_user(self, id):
        if id in self.id_to_user:
            return self.id_to_user[id]
        return "Unknown user"

    def post_message(self, text, channel="random"):
        try:
            response = self.client.chat_postMessage(
							channel=channel,
							text=text)
        except SlackApiError as e:
            print(e)
	
    def send_message_to_user(self, text, user_id="U06T4JLQHQR", channel="random"):
        try:
            return self.client.chat_postEphemeral(
							channel=channel, 
							text=text, 
							user=user_id)
        except SlackApiError as e:
            print(e)
	
    def isProviderAlive(self):
        try:
            response = self.client.api_test()
        except SlackApiError as e:
            print(e)

    async def pullData(self, start_time: datetime):
        try:  
            messages = []
            # Get a list of all channels
            channels_list = self.client.conversations_list()
            self.nzprint("List of all channels:\nCHANNEL ID\tCHANNEL NAME", len(channels_list['channels']), "channels")
            for channel in channels_list['channels']:
                self.id_to_channel[channel['id']] = channel['name']
                print(channel['id'], '\t', channel['name'], '\t',)
                self.history_json[channel['name']] = []
            print('\n')
        
            self.nzprint("There are " + str(len(self.id_to_channel)) + " channels in the workspace.", len(self.id_to_channel), "channels")
            for channel_id in self.id_to_channel.keys():
                try:  
                    # Get the members of the conversation
                    print("Channel: ", self.id_to_channel[channel_id])
                    conv_members = self.client.conversations_members(
                                    channel=channel_id)
                    self.nzprint(str(len(conv_members['members'])) + " members in the conversation: ", len(conv_members['members']), "members")

                    # Get the names of the members
                    for member in conv_members['members']:
                        if member not in self.id_to_user:
                            response = self.client.users_info(
                                            user=member)
                            self.id_to_user[member] = response['user']['real_name']
                        print(self.id_to_user[member])
                    print()

                    # Get the conversation history
                    response = self.client.conversations_history(
                                    channel=channel_id, oldest=self.convert_date_to_ts(start_time))
                    
                    # Check if there are any new messages
                    newStuff = False
                    for message in response['messages'][::-1]:
                        if not self.too_old(float(message['ts']), start_time):
                            newStuff = True
                            break
                        
                    # Print all the messages    
                    self.nzprint("Messages in the conversation: ", 1 if newStuff else 0, "new messages")
                    for message in response['messages'][::-1]:
                        if self.too_old(float(message['ts']), start_time):
                            continue
                        for user_id in self.id_to_user.keys():
                            message['text'] = message['text'].replace(f'<@{user_id}>', self.id_to_user[user_id])
                        print(f'{self.get_user(message["user"])} [{self.convert_ts_to_date(float(message['ts']))}]: {message["text"]}')
                        self.history_json[self.id_to_channel[channel_id]].append(
                            {'user': self.get_user(message['user']), 
                             'time': self.convert_ts_to_date(float(message['ts'])), 
                             'text': message['text']})
                        
                        message_chunk = Message()
                        message_chunk.id = channel_id + -'-' + message['ts']
                        message_chunk.user_id = message['user']
                        message_chunk.sender = self.get_user(message['user'])
                        message_chunk.message_content = message['text']
                        message_chunk.app = "Slack"
                        message_chunk.date = self.convert_ts_to_date(float(message['ts']))
                        messages.append(message_chunk)
                        
                    print()
                except:
                    print("The bot has not been added to channel ", self.id_to_channel[channel_id])
                    
            with open('history.json', 'w') as f:
                json.dump(self.history_json, f)
            return messages
        
        except SlackApiError as e:
            print(e)
  
if __name__ == "__main__":
    slack = SlackDataPull()
    slack.isProviderAlive()
    asyncio.run(slack.pullData(datetime.datetime(2024, 4, 20, 0, 0, 0)))
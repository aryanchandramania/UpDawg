import os
from slack_sdk import WebClient 
from slack_sdk.errors import SlackApiError 
import json
import datetime

""" We need to pass the 'Bot User OAuth Token' """
slack_token = 'xoxb-6909856229971-6912673347860-qclXgwLwCsjKLfycFF9J788f'

# Creating an instance of the Webclient class
client = WebClient(token=slack_token)

def convert_ts_to_date(ts):
	return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

def too_old(ts, time_delta):
	return datetime.datetime.now().timestamp() - float(ts) > time_delta * 60 * 60 * 24

id_to_channel = {}
def get_channel(id):
	if id in id_to_channel:
		return id_to_channel[id]
	return "Unknown channel"

id_to_user = {}
def get_user(id):
	if id in id_to_user:
		return id_to_user[id]
	return "Unknown user"

def post_message(text, channel="random"):
	try:
		response = client.chat_postMessage(
						channel=channel,
						text=text)
	except SlackApiError as e:
		print(e)
  
def send_message_to_user(text, user_id="U06T4JLQHQR", channel="random"):
	try:
		response = client.chat_postEphemeral(
						channel=channel, 
						text=text, 
						user=user_id)
	except SlackApiError as e:
		print(e)
  
history_json = {}

def get_conv_history(time_delta):
	try:  
		# Get a list of all channels
		print("List of all channels: ")
		print("CHANNEL ID\tCHANNEL NAME")
		channels_list = client.conversations_list()
		for channel in channels_list['channels']:
			id_to_channel[channel['id']] = channel['name']
			print(channel['id'], '\t', channel['name'], '\t',)
			history_json[channel['name']] = []
		print('\n')
  
		print("There are ", len(id_to_channel), " channels in the workspace.")
		for channel_id in id_to_channel.keys():
			# Get the members of the conversation
			print("Channel: ", id_to_channel[channel_id])
			conv_members = client.conversations_members(
							channel=channel_id)
			print(len(conv_members['members']), " members in the conversation: ")

			# Get the names of the members
			for member in conv_members['members']:
				if member in id_to_user:
					continue
				response = client.users_info(
								user=member)
				id_to_user[member] = response['user']['real_name']
				print(id_to_user[member])
			print()

			# Get the conversation history
			print("Messages in the conversation: ")
			response = client.conversations_history(
							channel=channel_id)
			for message in response['messages'][::-1]:
				if too_old(message['ts'], time_delta):
					continue
				for user_id in id_to_user.keys():
					message['text'] = message['text'].replace(f'<@{user_id}>', id_to_user[user_id])
				print(f'{get_user(message["user"])} [{convert_ts_to_date(float(message['ts']))}]: {message["text"]}')
				history_json[id_to_channel[channel_id]].append({'user': get_user(message['user']), 'time': convert_ts_to_date(float(message['ts'])), 'text': message['text']})
			print()
		print()
		with open('history.json', 'w') as f:
			json.dump(history_json, f)
		
	except SlackApiError as e:
		print(e)
  
if __name__ == "__main__":
	get_conv_history(1)
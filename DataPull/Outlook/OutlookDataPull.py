from configparser import SectionProxy
from azure.identity import DeviceCodeCredential
from msgraph import GraphServiceClient
from msgraph.generated.users.item.user_item_request_builder import UserItemRequestBuilder
from msgraph.generated.users.item.mail_folders.item.messages.messages_request_builder import (
    MessagesRequestBuilder)
from msgraph.generated.users.item.send_mail.send_mail_post_request_body import (
    SendMailPostRequestBody)
from msgraph.generated.models.message import Message
from msgraph.generated.models.item_body import ItemBody
from msgraph.generated.models.body_type import BodyType
from msgraph.generated.models.recipient import Recipient
from msgraph.generated.models.email_address import EmailAddress
import configparser
from datetime import datetime, timezone
import sys

sys.path.append('..')
from DataPull import DataPull
from Message.Message import Message



class OutlookDataPull():
    settings: SectionProxy
    device_code_credential: DeviceCodeCredential
    user_client: GraphServiceClient

    def __init__(self):
        # Load settings
        config = configparser.ConfigParser()
        config.read(['config.cfg', 'config.dev.cfg'])
        azure_settings = config['azure']
        self.settings = azure_settings

        client_id = self.settings['clientId']
        tenant_id = self.settings['tenantId']
        graph_scopes = self.settings['graphUserScopes'].split(' ')

        self.device_code_credential = DeviceCodeCredential(client_id, tenant_id = tenant_id)
        self.user_client = GraphServiceClient(self.device_code_credential, graph_scopes)
 

    # start_date needs to be a datetime object in UTC
    # this function is supposed to fetch data from start_date to current date
    # returns a list of dictionaries, each dictionary represents a message
    async def pullData(self, start_date):

        query_params = MessagesRequestBuilder.MessagesRequestBuilderGetQueryParameters(
            # Only request specific properties
            select=['id', 'from', 'receivedDateTime', 'subject', 'body'],
            # Sort by received time, newest first
            orderby=['receivedDateTime DESC'],
            filter = f"ReceivedDateTime ge {start_date.strftime('%Y-%m-%dT%H:%M:%SZ')}",
        )
        request_config = MessagesRequestBuilder.MessagesRequestBuilderGetRequestConfiguration(
            query_parameters= query_params
        )
        request_config.headers.add("Prefer", "outlook.body-content-type=\"text\"")

        messages = await self.user_client.me.mail_folders.by_mail_folder_id('inbox').messages.get(
                request_configuration=request_config)
        
        
        dataDump = []
        if messages and messages.value:
            # Output each message's details
            for message in messages.value:
                dataChunk = Message()
                if message.id:
                    dataChunk.id = message.id
                if message.subject:
                    dataChunk.message_content = f'Subject: {message.subject}\n\n'
                if (message.from_ and message.from_.email_address):
                    dataChunk.sender = message.from_.email_address.name
                if message.received_date_time:
                    dataChunk.date = message.received_date_time
                if message.body and message.body.content:
                    dataChunk.message_content += message.body.content
                
                # get current logged in user ID
                dataDump.append(dataChunk)
                print(dataChunk)
                
    
        return dataDump
    
    
    

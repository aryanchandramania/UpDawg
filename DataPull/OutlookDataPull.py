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



class OutlookDataPull(DataPull):
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
    async def pullData(self, start_date):
        # Get the current datetime in UTC
        current_datetime_utc = datetime.now(timezone.utc)



        query_params = MessagesRequestBuilder.MessagesRequestBuilderGetQueryParameters(
            # Only request specific properties
            select=['from', 'receivedDateTime', 'subject', 'body'],
            # Sort by received time, newest first
            orderby=['receivedDateTime DESC']
        )
        request_config = MessagesRequestBuilder.MessagesRequestBuilderGetRequestConfiguration(
            query_parameters= query_params
        )
        request_config.headers.add("Prefer", "outlook.body-content-type=\"text\"")

        messages = await self.user_client.me.mail_folders.by_mail_folder_id('inbox').messages.get(
                request_configuration=request_config)
        
        subject=None
        sender=None
        body=None
        receivedDateTime=None
        if messages and messages.value:
            # Output each message's details
            for message in messages.value:
                # subject
                subject = message.subject
                if (message.from_ and message.from_.email_address):
                    sender = message.from_.email_address.name
                receivedDateTime = message.received_date_time
                body = message.body.content
        
        comb = f'Subject: {subject}\n\n {body}'
        return messages
    
    
    

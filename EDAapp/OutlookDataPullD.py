# Outlook

import asyncio
import pika
from datetime import datetime, timezone
import json
import pytz

import sys
sys.path.append('../src')
from DataPull.Outlook.OutlookDataPull import OutlookDataPull



def start_outlook_publisher():

    puller = OutlookDataPull()
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    def async_callback(ch, method, properties, body):
        loop = asyncio.get_event_loop()
        print(" [x] Received request for Outlook data")
        body = json.loads(body.decode('utf-8'))

        startDate = pytz.utc.localize(datetime.strptime(body['startdate'], "%Y-%m-%d %H:%M:%S"))

        async def wrapper():
            messages = await puller.pullData(startDate)
            # parsing
            json_messages = [msg.to_dict() for msg in messages]
            if len(json_messages) == 0:
                json_messages = [{"app":"Outlook","NOTFOUND":"true"}]


            message = json.dumps(json_messages)
            channel.basic_publish(exchange='', routing_key='data_queue', body=message)

        loop.run_until_complete(wrapper())
        print(" [x] Data published to data queue")

    channel.basic_consume(queue='Outlook_request_queue', on_message_callback=async_callback, auto_ack=True)
    print(' [*] Waiting for requests from DataEngine. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == "__main__":
    start_outlook_publisher()



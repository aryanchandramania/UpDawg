# Data Engine


import pika
import json
from src.DataEngine.DataEngine import DataEngine
from src.DataClasses.MessageServices import MessageServices
from src.Message.Message import Message
from datetime import datetime, timezone
import pytz

def start_data_engine():
    # RabbitMQ setup
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    de = DataEngine()
    services = MessageServices()
    app_names = services.service_names
    chunks_received = {app_name: False for app_name in app_names}

    # date to start getting data from, from the db, for the user
    startDate = None

    # sends a rqeuest to data pullers to get data from a specific date
    # this startdate is basically the latest entry date
    def send_request_toPullData(key, startdate):
        # Send request for data
        # channel.basic_publish(exchange='', routing_key=key, body=json.dumps({'startdate': startdate}))
        channel.basic_publish(exchange='req_exchange', body=json.dumps({'startdate': startdate}))
        print(" [x] Sent request for pulling data")


    # this function is called as a callback when event comes from prompter
    # it process the startdate and stores it in the global variable
    # and it will pull gap data amount
    def getData_C(ch, method, properties, body):
        global startDate
        # parse startdate
        body = json.loads(body.decode('utf-8'))
        startDate = pytz.utc.localize(datetime.strptime(body['startdate'], "%Y-%m-%d %H:%M:%S"))


        latest_entries = de.checkGap()
        for app_name in app_names:
            if latest_entries[app_name] is not None:
                send_request_toPullData(f'{app_name}_request_queue',latest_entries[app_name].strftime("%Y-%m-%d %H:%M:%S"))
                # gapData = self.apps[app_name].pullData(latest_entries[app_name])
                

    # this is called when gap data is received from the data pullers
    # if all data has been received => it will process the data and send it to prompter
    def receiveChunk_C(ch, method, properties, body):
        global chunks_received
        print(" [x] Received data chunk")

        body = json.loads(body.decode('utf-8'))
        

        gapData=[]
        for msg in body:
            msgobj = Message()
            msgobj.from_dict(msg)
            gapData.append(msg)
        
        de.pushData(gapData)

      
        app_name = body[0]['app']
        chunks_received[app_name] = True

        # if both data chunks came through
        if all(chunks_received.values()):
            print(" [x] All data chunks received")
            final_data = de.getDataFromDB(startDate)

            # resetting
            chunks_received = {app_name: False for app_name in app_names}
            startDate = None

            # parse final data
            result = {}
            for app_name,msgs in final_data.items():
                result[app_name] = [msg.to_dict() for msg in msgs]

            # respond with data on the prompter channel
            channel.basic_publish(exchange='', routing_key='final_data_queue', body=json.dumps(result))
        

    channel.basic_consume(queue='data_queue', on_message_callback=receiveChunk_C, auto_ack=True)
    channel.basic_consume(queue='trigger_queue', on_message_callback=getData_C, auto_ack=True)
    print(' [*] Waiting for data from Slack and Outlook. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == "__main__":
    start_data_engine()
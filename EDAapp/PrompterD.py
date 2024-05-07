
import pika
import json

import sys
sys.path.append('../src')
from Message.Message import Message
from Prompter.Prompter import Prompter


def kick_off(startdate):

    # RabbitMQ setup
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    final_summary = None

    prmpt = Prompter('Summarize the following message data from various sources into a coherent format')

    channel.basic_publish(exchange='',routing_key='trigger_queue', body=json.dumps({'startdate':startdate.strftime("%Y-%m-%d %H:%M:%S")}))


    def handoffToLLM_C(ch, method, properties, body):
        print(" [x] Received data from DB")
        body = json.loads(body.decode('utf-8'))
        # print(body)
        # parse final data
        result = {}
        for app_name,msgs in body.items():
            for msg in msgs:
                msgobj = Message()
                msgobj.from_dict(msg)

                if app_name not in result:
                    result[app_name] = []

                result[app_name].append(msgobj)
        
        stringifiedPrompt = prmpt.prompt_contructor(result)
        channel.basic_publish(exchange='', routing_key='prompt_queue', body=json.dumps({'prompt':stringifiedPrompt,'sys_prompt':prmpt.summary_sys_prompt}))
        channel.basic_cancel(consumer_tag=method.consumer_tag)
        

    def handoffToResponseParser(ch, method, properties, body):
        nonlocal final_summary
        print(" [x] Received response from LLM")
        body = json.loads(body.decode('utf-8'))
        print(body['summary'])

        # give to response parser

        final_summary = body['summary']

        channel.basic_cancel(consumer_tag=method.consumer_tag)
        
        


    channel.basic_consume(queue='final_data_queue', on_message_callback=handoffToLLM_C, auto_ack=True)
    channel.basic_consume(queue='summary_queue', on_message_callback=handoffToResponseParser, auto_ack=True)
    print(' [*] Waiting for data from DB')
    channel.start_consuming()

    return final_summary
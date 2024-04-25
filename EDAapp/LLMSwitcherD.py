import pika
import json
from src.AdaService.AdaLLM import AdaLLM

def start_LLMSwitcher_engine():
    # RabbitMQ setup
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    adlm = AdaLLM()

    
    def summarize_C(ch, method, properties, body):
        print(" [x] Received data from Slack and Outlook")
        body = json.loads(body.decode('utf-8'))
        prompt = body['prompt']
        sys_prompt = body['sys_prompt']

        adlm.scoreLLM()
        summarizer = adlm.choose()
        summary = summarizer(prompt, sys_prompt)
        
        channel.basic_publish(exchange='', routing_key='summary_queue', body=json.dumps({'summary':summary}))

    

    channel.basic_consume(queue='prompt_queue', on_message_callback=summarize_C, auto_ack=True)
    print(' [*] Waiting for data from Slack and Outlook. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == "__main__":
    start_LLMSwitcher_engine()
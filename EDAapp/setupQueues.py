import pika

# RabbitMQ setup
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()


# Declare two queues between the DataEngine and the DataPull services
# req queue
channel.queue_declare(queue='Slack_request_queue')  # Queue for receiving requests from DataEngine
channel.queue_declare(queue='Outlook_request_queue')
channel.exchange_declare(exchange='req_exchange', exchange_type='fanout')
channel.queue_bind(exchange='req_exchange', queue='Slack_request_queue')
channel.queue_bind(exchange='req_exchange', queue='Outlook_request_queue')
# data queue
channel.queue_declare(queue='data_queue')     # Queue for sending data to DataEngine


# Declare two queues between Prompter and DataEngine
channel.queue_declare(queue='trigger_queue')
channel.queue_declare(queue='final_data_queue')


# Declare two queues between Prompter and LLM Switcher
channel.queue_declare(queue='prompt_queue')
channel.queue_declare(queue='summary_queue')
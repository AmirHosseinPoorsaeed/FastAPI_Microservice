import json
import os
import pika
from dotenv import load_dotenv


load_dotenv()


url = os.getenv('CLOUDAMPQ')
params = pika.URLParameters(url=url)
connection = pika.BlockingConnection(
    parameters=params
)
channel = connection.channel()

channel.queue_declare(queue='inventory')


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(
        exchange='',
        routing_key='inventory',
        body=json.dumps(body),
        properties=properties
    )

print('Message sent to cosumer')

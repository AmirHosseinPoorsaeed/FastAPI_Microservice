import pika
import os
from dotenv import load_dotenv

load_dotenv()


url = os.getenv('CLOUDAMPQ')
params = pika.URLParameters(url=url)
connection = pika.BlockingConnection(
    parameters=params
)
channel = connection.channel()

channel.queue_declare(queue='order')

def publish(body):
    channel.basic_publish(
        exchange='',
        routing_key='order',
        body=body
    )

print('Message sent to cosumer')

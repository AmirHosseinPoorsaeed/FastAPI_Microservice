import pika, sys, os
from dotenv import load_dotenv


load_dotenv()


def main():
    url = os.getenv('CLOUDAMPQ')
    params = pika.URLParameters(url=url)
    connection = pika.BlockingConnection(
        parameters=params
    )
    channel = connection.channel()

    channel.queue_declare(queue='order')

    def callback(ch, method, properties, body):
        print('received in order')
        print(body)

    channel.basic_consume(
        queue='order', 
        on_message_callback=callback, 
        auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

import json
import pika, sys, os
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from .. import database
from ..inventory import models

load_dotenv()


get_db = database.get_db


def main():
    url = os.getenv('CLOUDAMPQ')
    params = pika.URLParameters(url=url)
    connection = pika.BlockingConnection(
        parameters=params
    )
    channel = connection.channel()

    channel.queue_declare(queue='inventory')

    def callback(ch, method, properties, body):
        print('received in inventory')
        data = json.loads(body)
        db: Session = next(get_db())

        try:
            if properties.content_type == 'order_created':
                product = db.query(models.Product).\
                    filter(models.Product.id == data['product_id']).first()
                product.quantity = product.quantity - data['quantity']
                db.commit()
        except Exception as e:
            print(f"Error processing message: {e}")
            db.rollback()
        finally:
            db.close()
            

    channel.basic_consume(
        queue='inventory',
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




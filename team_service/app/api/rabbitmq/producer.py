import pika
import json
import time

RABBITMQ_URL = "amqp://user:pass@rabbitmq:5672/"

def send_message(exchange: str, routing_key: str, message: dict):
    max_retries = 5
    for attempt in range(max_retries):
        try:
            connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
            channel = connection.channel()
            channel.exchange_declare(exchange=exchange, exchange_type="direct")

            channel.basic_publish(
                exchange=exchange,
                routing_key=routing_key,
                body=json.dumps(message),
                properties=pika.BasicProperties(content_type='application/json')
            )
            connection.close()
            return
        except pika.exceptions.AMQPConnectionError as e:
            print(f"RabbitMQ connection failed: {e}. Retrying in 5 seconds...")
            time.sleep(5)
    raise Exception("Failed to connect to RabbitMQ after multiple retries")

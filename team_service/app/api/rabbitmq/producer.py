# team_service/rabbitmq/producer.py
import pika
import json

RABBITMQ_URL = "amqp://guest:guest@localhost:5672/"

def send_message(exchange: str, routing_key: str, message: dict):
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

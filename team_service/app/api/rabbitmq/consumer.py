import pika
import json

RABBITMQ_URL = "amqp://user:pass@rabbitmq:5672/"

def handle_message(ch, method, properties, body):
    message = json.loads(body)
    print(f"Received message: {message}")

    # Реализуйте логику обработки
    action = message.get("action")
    if action == "User Registered":
        username = message.get("username")
        print(f"User {username} has been registered!")

def start_consumer():
    connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
    channel = connection.channel()

    channel.exchange_declare(exchange="user_exchange", exchange_type='direct')
    queue = channel.queue_declare(queue="user_notifications", durable=True)
    channel.queue_bind(exchange="user_exchange", queue=queue.method.queue, routing_key="user.registered")

    channel.basic_consume(
        queue=queue.method.queue,
        on_message_callback=handle_message,
        auto_ack=True
    )

    print("Started consuming messages...")
    channel.start_consuming()

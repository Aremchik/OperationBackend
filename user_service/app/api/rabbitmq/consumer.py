# user_service/rabbitmq/consumer.py
import pika
import json
from sqlalchemy.ext.asyncio import AsyncSession
from api.database.database import get_db
from api.model.model import UserModel

RABBITMQ_URL = "amqp://guest:guest@localhost:5672/"

async def process_message(ch, method, properties, body):
    message = json.loads(body)
    action = message.get("action")
    user_id = message.get("user_id")
    team_id = message.get("team_id")

    if action == "add_user":
        async with get_db() as db:  # Получаем сессию
            user = await db.get(UserModel, user_id)
            if user:
                user.team = team_id
                await db.commit()
                print(f"Updated user {user_id} with team {team_id}")

def start_consuming():
    connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
    channel = connection.channel()

    channel.exchange_declare(exchange="team_exchange", exchange_type="direct")
    queue = channel.queue_declare(queue="", exclusive=True)
    channel.queue_bind(exchange="team_exchange", queue=queue.method.queue, routing_key="team.user_update")

    channel.basic_consume(queue=queue.method.queue, on_message_callback=process_message, auto_ack=True)
    print("Listening for messages...")
    channel.start_consuming()

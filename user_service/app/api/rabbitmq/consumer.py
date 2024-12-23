import pika
import json
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.database.database import get_db
from app.api.model.model import UserModel

RABBITMQ_URL = "amqp://user:pass@rabbitmq:5672/"

async def process_message(ch, method, properties, body):
    try:
        message = json.loads(body)
        action = message.get("action")
        user_id = message.get("user_id")
        team_id = message.get("team_id")

        if action == "add_user" and user_id and team_id:
            async with get_db() as db: 
                user = await db.get(UserModel, user_id)
                if user:
                    user.team = team_id
                    await db.commit()
                    print(f"Updated user {user_id} with team {team_id}")
                else:
                    print(f"User with ID {user_id} not found.")
    except Exception as e:
        print(f"Error processing message: {e}")

def start_consuming():
    connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
    channel = connection.channel()

    channel.exchange_declare(exchange="team_exchange", exchange_type="direct")
    queue = channel.queue_declare(queue="team_user_update_queue", durable=True)
    channel.queue_bind(exchange="team_exchange", queue=queue.method.queue, routing_key="team.user_update")

    channel.basic_consume(
        queue=queue.method.queue,
        on_message_callback=lambda ch, method, properties, body: pika.adapters.utils.connection.BlockingConnection.run_coroutine_threadsafe(
            process_message(ch, method, properties, body), None
        ).result(),
        auto_ack=True
    )

    print("Listening for messages...")
    channel.start_consuming()

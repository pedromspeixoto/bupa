import redis
import uuid
import datetime
import os
import json

# Connect to Redis
if os.getenv("CONVERSATION_HISTORY")=="true":

    # Check if redis host is set
    if os.getenv("REDIS_HOST") is None:
        redis_host = "localhost"
    else:
        redis_host = os.getenv("REDIS_HOST")

    if os.getenv("REDIS_PORT") is None:
        redis_port = "6379"
    else:
        redis_port = os.getenv("REDIS_PORT")

    redis_client = redis.Redis(host=redis_host, port=int(redis_port), db=0)
else:
    redis_client = None

def save_message(conversation_key, message_type, message):
    # Ensure that the conversation key is a string and is not None
    conversation_key = str(conversation_key)

    if conversation_key is None:
        raise ValueError("Conversation key cannot be None")

    # Ensure message type is user or assistant
    if message_type not in ["user", "assistant"]:
        raise ValueError("Message type must be either 'user' or 'assistant'")

    # Ensure message is a string and is not None
    message = str(message)
    if message is None:
        raise ValueError("Message cannot be None")

    # Generate a unique identifier for the message
    message_id = str(uuid.uuid4())

    # Create a message dictionary
    message_data = {
        "id": message_id,
        "type": message_type,
        "message": message
    }

    # Push the message into the conversation list
    redis_client.rpush(conversation_key, json.dumps(message_data))

    # Set the expiration time for the conversation key
    expiration_time = datetime.datetime.now() + datetime.timedelta(days=1)
    redis_client.expireat(conversation_key, expiration_time)

    return message_id

def get_messages(conversation_key, num_messages):
    # Get the specified number of messages in the conversation list
    message_data = redis_client.lrange(conversation_key, 0, num_messages - 1)

    # Convert the message data to a list of dictionaries
    messages = []
    for data in message_data:
        message = json.loads(data)
        messages.append(message)

    return messages

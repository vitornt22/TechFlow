import json
from app import redis_client

QUEUE_NAME = "products_queue"


def enqueue_product_operation(operation, data):
    message = {
        "operation": operation,
        "data": data
    }
    redis_client.rpush(QUEUE_NAME, json.dumps(message))

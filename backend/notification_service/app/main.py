import asyncio
import json
from fastapi import FastAPI
import aio_pika
import os

app = FastAPI()

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://user:password@rabbitmq:5672/")

async def consume():
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    channel = await connection.channel()
    queue = await channel.declare_queue("notifications", durable=True)

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                data = json.loads(message.body.decode())
                print(f"[Notification Service] Received notification task: {data}")

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(consume())

@app.get("/")
async def root():
    return {"message": "Notification service running"}

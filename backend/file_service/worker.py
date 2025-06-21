import os
import asyncio
from aio_pika import connect_robust, IncomingMessage

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "user")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "password")

async def on_message(message: IncomingMessage):
    async with message.process():
        filename = message.body.decode()
        print(f"Received task to process file: {filename}")
        await asyncio.sleep(1)  
        print(f"Finished processing file: {filename}")

async def main():
    connection = await connect_robust(
        host=RABBITMQ_HOST,
        login=RABBITMQ_USER,
        password=RABBITMQ_PASS,
    )
    channel = await connection.channel()
    queue = await channel.declare_queue("file_tasks", durable=True)
    await queue.consume(on_message)

    print("Worker started. Waiting for messages...")
    await asyncio.Future()  

if __name__ == "__main__":
    asyncio.run(main())

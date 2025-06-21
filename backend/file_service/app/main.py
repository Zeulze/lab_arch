# file_service/app/main.py
from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from fastapi.responses import FileResponse
from app.auth import verify_token
import shutil
import os
import asyncio
import aio_pika
import json

app = FastAPI(root_path="/file")

UPLOAD_DIR = "./uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://user:password@rabbitmq:5672/")
async def get_rabbitmq_connection():
    return await aio_pika.connect_robust(RABBITMQ_URL)

async def publish_message(message: dict):
    connection = await get_rabbitmq_connection()
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue("file_tasks", durable=True)
        await channel.default_exchange.publish(
            aio_pika.Message(body=json.dumps(message).encode()),
            routing_key=queue.name
        )
        
async def publish_notification(message: dict):
    connection = await get_rabbitmq_connection()
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue("notification_tasks", durable=True)
        await channel.default_exchange.publish(
            aio_pika.Message(body=json.dumps(message).encode()),
            routing_key=queue.name
        )

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...), user_email: str = Depends(verify_token)):
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    await publish_message({
        "filename": file.filename,
        "uploaded_by": user_email
    })

    await publish_notification({
        "type": "file_uploaded",
        "filename": file.filename,
        "user": user_email,
        "message": f"File '{file.filename}' uploaded by {user_email}"
    })

    return {"filename": file.filename, "uploaded_by": user_email}


@app.get("/download/{filename}")
async def download_file(filename: str, user_email: str = Depends(verify_token)):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path=file_path, filename=filename, media_type='application/octet-stream')


async def consume():
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    channel = await connection.channel()
    queue = await channel.declare_queue("file_tasks", durable=True)

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                data = json.loads(message.body.decode())
                print(f"Received task: {data}")

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(consume())

from fastapi import FastAPI
from app.routes import auth_routes
from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(root_path="/auth")

app.include_router(auth_routes.router)
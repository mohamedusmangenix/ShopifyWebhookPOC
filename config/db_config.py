import os
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from contextlib import asynccontextmanager

MONGO_URL = os.getenv("MONGODB_URI")

client = AsyncIOMotorClient(MONGO_URL)


# explicitly define database name here
db: AsyncIOMotorDatabase = client["AltuxDXPOC"]
async def get_db():
    try:
        yield db
    finally:
        pass

@asynccontextmanager
async def get_db_context():
    try:
        yield db
    finally:
        pass

async def close_db():
    client.close()
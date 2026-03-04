from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorDatabase
from models.webhook_event_model import WebhookEvent

class WebhookEventService:

    @staticmethod
    async def save_event(topic: str, shop_domain: str, payload: dict, db: AsyncIOMotorDatabase):
        try:
            document = {
                "topic": topic,
                "shop_domain": shop_domain,
                "payload": payload,
                "received_at": datetime.now(timezone.utc),
            }
            result = await db["webhook_events"].insert_one(document)
            document["_id"] = str(result.inserted_id)
            return True, document
        except Exception as e:
            return False, str(e)

    @staticmethod
    async def get_event_list(db: AsyncIOMotorDatabase):
        try:
            cursor = db["webhook_events"].find()
            events = await cursor.to_list(length=None)
            for event in events:
                event["_id"] = str(event["_id"])
            if not events:
                return False, "No webhook events found"
            return True, events
        except Exception as e:
            return False, str(e)

    @staticmethod
    async def get_event_by_id(event_id: str, db: AsyncIOMotorDatabase):
        try:
            from bson import ObjectId
            event = await db["webhook_events"].find_one({"_id": ObjectId(event_id)})
            if not event:
                return False, "Webhook event not found"
            event["_id"] = str(event["_id"])
            return True, event
        except Exception as e:
            return False, str(e)
        
    @staticmethod
    async def get_event_by_webId(event_id: int, db: AsyncIOMotorDatabase):
        try:
            from bson import ObjectId
            event = await db["webhook_events"].find_one({"payload.id": event_id})
            if not event:
                return False, "Webhook event not found"
            event["_id"] = str(event["_id"])
            return True, event
        except Exception as e:
            return False, str(e)

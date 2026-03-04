from datetime import datetime
from typing import Optional, Any
from bson import ObjectId


class WebhookEvent:
    __collection__ = "webhook_events"

    id: ObjectId
    topic: str
    shop_domain: str
    payload: dict
    received_at: datetime

    def __init__(
        self,
        topic: str,
        shop_domain: str,
        payload: dict,
        received_at: datetime = None,
        id: Optional[ObjectId] = None
    ):
        self.id = id or ObjectId()
        self.topic = topic
        self.shop_domain = shop_domain
        self.payload = payload
        self.received_at = received_at or datetime.utcnow()

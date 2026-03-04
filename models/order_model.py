from datetime import datetime
from typing import Optional, List
from bson import ObjectId

class Order:
    __tablename__ = "orders"
    
    id: ObjectId
    order_id: str
    customer_name: str
    customer_email: str
    total_price: float
    currency: str
    status: str
    items: List[dict]
    created_at: datetime
    updated_at: datetime
    
    def __init__(
        self,
        order_id: str,
        customer_name: str,
        customer_email: str,
        total_price: float,
        currency: str = "USD",
        status: str = "pending",
        items: List[dict] = None,
        created_at: datetime = None,
        updated_at: datetime = None,
        id: Optional[ObjectId] = None
    ):
        self.id = id or ObjectId()
        self.order_id = order_id
        self.customer_name = customer_name
        self.customer_email = customer_email
        self.total_price = total_price
        self.currency = currency
        self.status = status
        self.items = items or []
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
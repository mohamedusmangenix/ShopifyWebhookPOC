from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime, timezone


class OrderService:

    @staticmethod
    async def get_order_list(db: AsyncIOMotorDatabase):
        try:
            cursor = db["orders"].find()
            orders = await cursor.to_list(length=None)
            for order in orders:
                order["_id"] = str(order["_id"])
            if not orders:
                return False, "No orders found"
            return True, orders
        except Exception as e:
            return False, str(e)

    @staticmethod
    async def get_order_by_id(order_id: str, db: AsyncIOMotorDatabase):
        try:
            order = await db["orders"].find_one({"order_id": order_id})
            if not order:
                return False, "Order not found"
            order["_id"] = str(order["_id"])
            return True, order
        except Exception as e:
            return False, str(e)

    @staticmethod
    async def create_order(payload: dict, db: AsyncIOMotorDatabase):
        try:
            payload["created_at"] = datetime.now(timezone.utc)
            payload["updated_at"] = datetime.now(timezone.utc)
            result = await db["orders"].insert_one(payload)
            payload["_id"] = str(result.inserted_id)
            return True, payload
        except Exception as e:
            return False, str(e)

    @staticmethod
    async def update_order(order_id: str, payload: dict, db: AsyncIOMotorDatabase):
        try:
            payload["updated_at"] = datetime.now(timezone.utc)
            result = await db["orders"].update_one(
                {"order_id": order_id},
                {"$set": payload}
            )
            if result.matched_count == 0:
                return False, "Order not found"
            updated = await db["orders"].find_one({"order_id": order_id})
            updated["_id"] = str(updated["_id"])
            return True, updated
        except Exception as e:
            return False, str(e)

    @staticmethod
    async def delete_order(order_id: str, db: AsyncIOMotorDatabase):
        try:
            result = await db["orders"].delete_one({"order_id": order_id})
            if result.deleted_count == 0:
                return False, "Order not found"
            return True, "Order deleted successfully"
        except Exception as e:
            return False, str(e)

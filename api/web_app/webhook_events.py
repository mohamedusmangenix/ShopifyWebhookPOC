from fastapi import APIRouter, Depends, Request
from motor.motor_asyncio import AsyncIOMotorDatabase

from config.db_config import get_db
from schemas.response_model import ResponseModel
from services.webhook_event_service import WebhookEventService

webhook_events_router = APIRouter()


@webhook_events_router.post("/notify", response_model=ResponseModel)
async def receive_notification(request: Request, db: AsyncIOMotorDatabase = Depends(get_db)):
    try:
        payload = await request.json()
        topic = payload.get("topic", "generic")
        shop_domain = payload.get("shop_domain", "unknown")

        status, result = await WebhookEventService.save_event(
            topic=topic,
            shop_domain=shop_domain,
            payload=payload,
            db=db,
        )
        if not status:
            return ResponseModel(
                data=None,
                status="Failed",
                is_success=False,
                message=result
            )
        return ResponseModel(
            data=result,
            status="Success",
            is_success=True,
            message="Notification saved successfully"
        )
    except Exception as e:
        return ResponseModel(
            data=None,
            status="Error",
            is_success=False,
            message=str(e)
        )


@webhook_events_router.get("/getEventList", response_model=ResponseModel)
async def get_event_list(db: AsyncIOMotorDatabase = Depends(get_db)):
    try:
        status, events = await WebhookEventService.get_event_list(db=db)
        if not status:
            return ResponseModel(
                data=None,
                status="No record found",
                is_success=False,
                message=events
            )
        return ResponseModel(
            data=events,
            status="Success",
            is_success=True,
            message="Webhook events retrieved successfully"
        )
    except Exception as e:
        return ResponseModel(
            data=None,
            status="Error",
            is_success=False,
            message=str(e)
        )


@webhook_events_router.get("/getEventById/{event_id}", response_model=ResponseModel)
async def get_event_by_id(event_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    try:
        status, event = await WebhookEventService.get_event_by_id(event_id=event_id, db=db)
        if not status:
            return ResponseModel(
                data=None,
                status="No record found",
                is_success=False,
                message=event
            )
        return ResponseModel(
            data=event,
            status="Success",
            is_success=True,
            message="Webhook event retrieved successfully"
        )
    except Exception as e:
        return ResponseModel(
            data=None,
            status="Error",
            is_success=False,
            message=str(e)
        )

import hashlib
import hmac
import base64
import json
import logging

from fastapi import APIRouter, Header, HTTPException, Request

from api.web_app.orders import orders_router
from api.web_app.webhook_events import webhook_events_router
from config.api_config import Config
from config.db_config import db
from services.webhook_event_service import WebhookEventService

logger = logging.getLogger(__name__)

api_router = APIRouter()

api_router.include_router(orders_router, prefix="/orders", tags=["orders"])
api_router.include_router(webhook_events_router, prefix="/webhook-events", tags=["webhook-events"])


def verify_shopify_webhook(body: bytes, hmac_header: str) -> bool:
    digest = hmac.new(Config.SHOPIFY_WEBHOOK_SECRET.encode(), body, hashlib.sha256).digest()
    computed = base64.b64encode(digest).decode()
    return hmac.compare_digest(computed, hmac_header)


@api_router.get("/health", tags=["health"])
def health():
    return {"status": "ok"}


@api_router.post("/webhooks/shopify", tags=["webhooks"])
async def shopify_webhook(
    request: Request,
    x_shopify_hmac_sha256: str = Header(...),
    x_shopify_topic: str = Header(...),
    x_shopify_shop_domain: str = Header(...),
):
    body = await request.body()

    if not verify_shopify_webhook(body, x_shopify_hmac_sha256):
        logger.warning("Invalid HMAC signature — request rejected")
        raise HTTPException(status_code=403, detail="Invalid signature")

    payload = json.loads(body)

    logger.info("Received webhook | topic=%s | shop=%s", x_shopify_topic, x_shopify_shop_domain)

    saved, result = await WebhookEventService.save_event(
        topic=x_shopify_topic,
        shop_domain=x_shopify_shop_domain,
        payload=payload,
        db=db,
    )
    if not saved:
        logger.error("Failed to save webhook event: %s", result)
    else:
        logger.info("Webhook event saved | _id=%s", result.get("_id"))

    if x_shopify_topic == "orders/create":
        _handle_order_created(payload)
    elif x_shopify_topic == "orders/updated":
        _handle_order_updated(payload)
    elif x_shopify_topic == "products/create":
        _handle_product_created(payload)
    else:
        logger.info("Unhandled topic: %s", x_shopify_topic)

    return {"received": True}


def _handle_order_created(payload: dict):
    logger.info("New order #%s | email=%s | total=%s",
                payload.get("id"), payload.get("email"), payload.get("total_price"))


def _handle_order_updated(payload: dict):
    logger.info("Order updated #%s | financial_status=%s",
                payload.get("id"), payload.get("financial_status"))


def _handle_product_created(payload: dict):
    logger.info("New product #%s | title=%s",
                payload.get("id"), payload.get("title"))

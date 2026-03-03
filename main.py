import hashlib
import hmac
import base64
import json
import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException, Request

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Shopify Webhook POC")

SHOPIFY_WEBHOOK_SECRET = os.getenv("SHOPIFY_WEBHOOK_SECRET", "")


def verify_shopify_webhook(body: bytes, hmac_header: str) -> bool:
    """Verify the webhook came from Shopify using HMAC-SHA256."""
    digest = hmac.new(SHOPIFY_WEBHOOK_SECRET.encode(), body, hashlib.sha256).digest()
    computed = base64.b64encode(digest).decode()
    return hmac.compare_digest(computed, hmac_header)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/webhooks/shopify")
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
    logger.info("Payload: %s", json.dumps(payload, indent=2))

    # Route to topic-specific handlers
    if x_shopify_topic == "orders/create":
        handle_order_created(payload)
    elif x_shopify_topic == "orders/updated":
        handle_order_updated(payload)
    elif x_shopify_topic == "products/create":
        handle_product_created(payload)
    else:
        logger.info("Unhandled topic: %s", x_shopify_topic)

    # Always return 200 quickly — Shopify retries on non-2xx
    return {"received": True}


def handle_order_created(payload: dict):
    order_id = payload.get("id")
    email = payload.get("email")
    total = payload.get("total_price")
    logger.info("New order #%s | email=%s | total=%s", order_id, email, total)


def handle_order_updated(payload: dict):
    order_id = payload.get("id")
    status = payload.get("financial_status")
    logger.info("Order updated #%s | financial_status=%s", order_id, status)


def handle_product_created(payload: dict):
    product_id = payload.get("id")
    title = payload.get("title")
    logger.info("New product #%s | title=%s", product_id, title)

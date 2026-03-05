import hashlib
import hmac
import base64
import json
import logging

from fastapi import APIRouter, Header, HTTPException, Request

from api.web_app.orders import orders_router
from api.web_app.webhook_events import webhook_events_router
from api.web_app.authorize import auth_app  
from config.api_config import Config
from config.db_config import db
from services.webhook_event_service import WebhookEventService


logger = logging.getLogger(__name__)

api_router = APIRouter()

api_router.include_router(orders_router, prefix="/orders", tags=["orders"])
api_router.include_router(webhook_events_router, prefix="/webhook-events", tags=["webhook-events"])
api_router.include_router(auth_app, prefix="/auth", tags=["authorize"])
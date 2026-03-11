import os
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime, timezone
import httpx

class AuthorizeService:
    async def generate_shopify_token(db: AsyncIOMotorDatabase):
        try:
            url = f"https://venkatscammer.myshopify.com/admin/oauth/access_token"

            params = {
                "grant_type": "client_credentials",
                "client_id": os.getenv("client_id"),
                "client_secret": os.getenv("client_secret")
            }

            async with httpx.AsyncClient() as client:
                response = await client.post(url, params=params)

            if response.status_code != 200:
                return False, f"Shopify API Error: {response.text}", None

            data = response.json()

            access_token = data.get("access_token")
            expires_in = data.get("expires_in", 86399)

            if not access_token:
                return False, "Access token not received", None

            current_time = datetime.now(timezone.utc)

            token_data = {

                "access_token": access_token,
                "created_at": current_time.timestamp(),
                "expires_in": current_time.timestamp() + expires_in
            }

            save_status, save_message = await AuthorizeService.save_token(db, access_token, expires_in)

            if not save_status:
                return False, f"Failed to save token: {save_message}", None
         
            return True, "Token generated successfully", token_data

        except httpx.RequestError as e:
            return False, f"HTTP Request failed: {str(e)}", None

        except Exception as e:
            return False, f"Unexpected error: {str(e)}", None

    @staticmethod
    async def validate_token( db: AsyncIOMotorDatabase):
        try:
            current_time = datetime.now(timezone.utc)

            token_data = await db["tokens"].find_one({})

            if not token_data:
                return False, "Token not found", None

            if token_data["expires_in"] < current_time.timestamp():
                status,message,token_data = await AuthorizeService.generate_shopify_token(db=db)
                if not status:
                     return False, message, None
                return True, "Token refreshed successfully", token_data

            return True, "Token is valid", token_data

        except Exception as e:
            return False, str(e), None
        
    @staticmethod        
    async def save_token(db, access_token, expires_in):
        try:
            current_time = datetime.now(timezone.utc)

            token_data = {
                "access_token": access_token,
                "created_at": current_time.timestamp(),
                "expires_in": current_time.timestamp() + expires_in
            }

            await db["tokens"].delete_many({})  # optional if only one token needed
            await db["tokens"].insert_one(token_data)

            return True, "Token saved successfully"

        except Exception as e:
            return False, str(e)
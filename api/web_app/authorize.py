from fastapi import FastAPI,Depends,APIRouter
from motor.motor_asyncio import AsyncIOMotorDatabase
from config.db_config import get_db
from schemas.response_model import ResponseModel
from services.authorize_service import AuthorizeService


auth_app = APIRouter()

@auth_app.post("/generateToken", response_model=ResponseModel)
async def generate_token(db: AsyncIOMotorDatabase = Depends(get_db)):
    try:
        status,message,token_data = await AuthorizeService.generate_shopify_token(db=db)
        if not status:
            return ResponseModel(
                data=None,
                status=message,
                is_success=False,
                message=message
                )
        return ResponseModel(
            data={"token": token_data.get("access_token"),
                   "expires_in": token_data.get("expires_in")
            },
            status="Token generated successfully",
            is_success=True,
            message="Token generated successfully"
            )
    except Exception as e:
        return ResponseModel(
            data=None,
            status="Error occurred",
            is_success=False,
            message=str(e)
            )

@auth_app.get("/validateToken", response_model=ResponseModel)
async def validate_token(db: AsyncIOMotorDatabase = Depends(get_db)):
    try:
        status,message,token_data = await AuthorizeService.validate_token(db=db)
        if not status:
            return ResponseModel(
                data=None,
                status=message,
                is_success=False,
                message=message
            )
        if not token_data:
            return ResponseModel(
                data=None,
                status="No record found",
                is_success=False,
                message="Token not found"
            )
        return ResponseModel(
            data={"token": token_data.get("access_token"),
                   "expires_in": token_data.get("expires_in")
            },
            status="Token is valid",
            is_success=True,
            message="Token is valid"
        )
    except Exception as e:
        return ResponseModel(
                data=None,
                status="Error occurred",
                is_success=False,
                message=str(e)
            )
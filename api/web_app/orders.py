from fastapi import APIRouter, BackgroundTasks, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from config.db_config import get_db
from schemas.response_model import ResponseModel
from services.order_service import OrderService

orders_router = APIRouter()


@orders_router.get("/getOrderList", response_model=ResponseModel)
async def get_order_list(background_tasks: BackgroundTasks, db: AsyncIOMotorDatabase = Depends(get_db)):
    try:
        status, orders = await OrderService.get_order_list(db=db)
        if not status:
            return ResponseModel(
                data=None,
                status="No record found",
                is_success=False,
                message=orders
            )
        return ResponseModel(
            data=orders,
            status="Success",
            is_success=True,
            message="Orders retrieved successfully"
        )
    except Exception as e:
        return ResponseModel(
            data=None,
            status="Error",
            is_success=False,
            message=str(e)
        )


@orders_router.get("/getOrderById/{order_id}", response_model=ResponseModel)
async def get_order_by_id(order_id: str, background_tasks: BackgroundTasks, db: AsyncIOMotorDatabase = Depends(get_db)):
    try:
        status, order = await OrderService.get_order_by_id(order_id=order_id, db=db)
        if not status:
            return ResponseModel(
                data=None,
                status="No record found",
                is_success=False,
                message=order
            )
        return ResponseModel(
            data=order,
            status="Success",
            is_success=True,
            message="Order retrieved successfully"
        )
    except Exception as e:
        return ResponseModel(
            data=None,
            status="Error",
            is_success=False,
            message=str(e)
        )


@orders_router.post("/createOrder", response_model=ResponseModel)
async def create_order(payload: dict, background_tasks: BackgroundTasks, db: AsyncIOMotorDatabase = Depends(get_db)):
    try:
        status, order = await OrderService.create_order(payload=payload, db=db)
        if not status:
            return ResponseModel(
                data=None,
                status="Failed",
                is_success=False,
                message=order
            )
        return ResponseModel(
            data=order,
            status="Success",
            is_success=True,
            message="Order created successfully"
        )
    except Exception as e:
        return ResponseModel(
            data=None,
            status="Error",
            is_success=False,
            message=str(e)
        )


@orders_router.put("/updateOrder/{order_id}", response_model=ResponseModel)
async def update_order(order_id: str, payload: dict, background_tasks: BackgroundTasks, db: AsyncIOMotorDatabase = Depends(get_db)):
    try:
        status, order = await OrderService.update_order(order_id=order_id, payload=payload, db=db)
        if not status:
            return ResponseModel(
                data=None,
                status="No record found",
                is_success=False,
                message=order
            )
        return ResponseModel(
            data=order,
            status="Success",
            is_success=True,
            message="Order updated successfully"
        )
    except Exception as e:
        return ResponseModel(
            data=None,
            status="Error",
            is_success=False,
            message=str(e)
        )


@orders_router.delete("/deleteOrder/{order_id}", response_model=ResponseModel)
async def delete_order(order_id: str, background_tasks: BackgroundTasks, db: AsyncIOMotorDatabase = Depends(get_db)):
    try:
        status, message = await OrderService.delete_order(order_id=order_id, db=db)
        if not status:
            return ResponseModel(
                data=None,
                status="No record found",
                is_success=False,
                message=message
            )
        return ResponseModel(
            data=None,
            status="Success",
            is_success=True,
            message=message
        )
    except Exception as e:
        return ResponseModel(
            data=None,
            status="Error",
            is_success=False,
            message=str(e)
        )

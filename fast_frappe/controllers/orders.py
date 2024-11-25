from fastapi.responses import JSONResponse
from fastapi import APIRouter
import frappe

from fast_frappe.ctrl import init_frappe
from restaurant.public_api import get_orders as fetch_orders
from fast_frappe.serializers.orders import Order


router = APIRouter()


@router.get('/get_orders/')
def get_orders(server_id: str | None = None):
    """
    Retrieve an orders filtered per Server.

    - **server_id**: The ID of the server with which to filter orders to retrieve. Optional.
    """
    init_frappe()
    data = fetch_orders(server_id=None)
    return JSONResponse(content=data)


@router.post("/create_order")
async def create_order(order: Order):
    init_frappe()
    order_doc = frappe.get_doc({
        "doctype": "Order",
        "table": order.table,
        "status": order.status,
        "currency": order.currency,
        "subtotal": order.subtotal,
        "tax": order.tax,
        "total": order.total,
        "server": order.server,
        "payment_status": order.payment_status,
        "items": [dict(item) for item in order.items],
        "subtotal": order.subtotal,
        "tax": order.tax,
        "total": order.total,
        "server": order.server,
        "payment_status": order.payment_status
    })
    
    # Save the document
    order_doc.insert()
    frappe.db.commit()
    
    return JSONResponse(
        status_code=201,
        content={"message": "Order created successfully", "order_id": order_doc.name}
    )


@router.patch("/update_order/{order_id}")
async def update_order(order_id: str, order:Order):
    pass


@router.delete("/delete_order/{order_id}")
async def delete_order(order_id: str, order:Order):
    pass


@router.get("/get_order/{order_id}")
async def get_order(order_id: str, order:Order):
    pass